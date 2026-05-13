<template>
  <div class="items-page">
    <!-- Filter Toolbar -->
    <div class="filter-toolbar">
      <input 
        v-model="searchQuery" 
        class="search-input" 
        placeholder="🔎  Search by item name, location..."
        @input="applyFilters"
      />
      <select v-model="filterCategory" @change="applyFilters" class="filter-select">
        <option value="">All Categories</option>
        <option>Electronics</option>
        <option>ID/Cards</option>
        <option>Clothing</option>
        <option>Accessories</option>
        <option>Books</option>
        <option>Keys</option>
        <option>Other</option>
      </select>
      <select v-model="filterStatus" @change="applyFilters" class="filter-select">
        <option value="">All Status</option>
        <option>Lost</option>
        <option>Found</option>
        <option>Claimed</option>
      </select>
      <select v-model="filterLocation" @change="applyFilters" class="filter-select">
        <option value="">All Buildings</option>
        <option>Adriatico</option>
        <option>Alingal</option>
        <option>Arrupe</option>
        <option>Belardo</option>
        <option>Bonoan</option>
        <option>Burns</option>
        <option>Chapel</option>
        <option>Covered Courts</option>
        <option>Dolan</option>
        <option>Grounds</option>
        <option>Library</option>
        <option>Phelan</option>
        <option>Richards</option>
        <option>Santos</option>
        <option>Xavier Hall</option>
      </select>
      <router-link to="/report" class="btn-add">+ Report Item</router-link>
    </div>

    <!-- Edit Form -->
    <div v-if="showForm" class="report-form-container">
      <h3>{{ editingId ? 'Edit Report' : 'New Report' }}</h3>
      <div class="form-grid">
        <div class="form-group">
          <label>Item Name *</label>
          <input v-model="form.name" class="form-input" placeholder="e.g. Black Jansport Backpack" />
        </div>
        <div class="form-group">
          <label>Category *</label>
          <select v-model="form.category" class="form-input">
            <option value="">Select Category...</option>
            <option>Electronics</option>
            <option>ID/Cards</option>
            <option>Clothing</option>
            <option>Accessories</option>
            <option>Books</option>
            <option>Keys</option>
            <option>Other</option>
          </select>
        </div>
        <div class="form-group">
          <label>Report Type</label>
          <select v-model="form.report_type" class="form-input">
            <option>Lost</option>
            <option>Found</option>
          </select>
        </div>
        <div class="form-group">
          <label>Date *</label>
          <input v-model="form.date_reported" type="date" class="form-input" />
        </div>
        <div class="form-group full-width">
          <label>Location *</label>
          <select v-model="form.location" class="form-input">
            <option value="">Select Building...</option>
            <option>Adriatico</option>
            <option>Alingal</option>
            <option>Arrupe</option>
            <option>Belardo</option>
            <option>Bonoan</option>
            <option>Burns</option>
            <option>Chapel</option>
            <option>Covered Courts</option>
            <option>Dolan</option>
            <option>Grounds</option>
            <option>Library</option>
            <option>Phelan</option>
            <option>Richards</option>
            <option>Santos</option>
            <option>Xavier Hall</option>
          </select>
        </div>

        <!-- Image Upload with Preview -->
        <div class="form-group full-width">
          <label>Item Images (optional, max 5)</label>

          <!-- Existing images when editing -->
          <div v-if="editingId && form.existingImages?.length" class="image-preview-row">
            <div v-for="(img, index) in form.existingImages" :key="'existing-' + index" class="preview-thumb">
              <img :src="`http://127.0.0.1:5000/api/items/uploads/${img}`" class="thumb-img" />
            </div>
            <p class="preview-hint">⚠️ Uploading new images will replace these.</p>
          </div>

          <input
            type="file"
            @change="onFileSelected"
            class="form-input"
            accept="image/*"
            multiple
            :key="fileInputKey"
          />

          <!-- New file previews -->
          <div v-if="selectedFiles.length" class="image-preview-row" style="margin-top:8px;">
            <div v-for="(file, index) in selectedFiles" :key="'new-' + index" class="preview-thumb">
              <img :src="getPreviewUrl(file)" class="thumb-img" style="border-color:#5c6bc0;" />
              <button class="thumb-remove" @click="removeSelectedFile(index)">✕</button>
            </div>
            <p class="preview-hint" style="color:#5c6bc0;">{{ selectedFiles.length }} file(s) selected</p>
          </div>
        </div>

        <div class="form-group full-width">
          <label>Description</label>
          <textarea v-model="form.description" class="form-textarea" placeholder="Describe the item..."></textarea>
        </div>
        <div class="form-group full-width">
          <label>Contact Info</label>
          <input v-model="form.contact_info" class="form-input" placeholder="Phone or email" />
        </div>
      </div>
      <div class="form-buttons">
        <button class="btn-submit" @click="editingId ? updateItem() : createItem()">
          {{ editingId ? 'Save Changes' : 'Submit' }}
        </button>
        <button class="btn-cancel" @click="cancelEdit">Cancel</button>
      </div>
    </div>

    <!-- Items Grid -->
    <div class="items-grid">
      <div
        v-for="item in filteredItems"
        :key="item.item_id"
        class="item-card"
        :class="{ clickable: !isItemOwner(item) }"
        @click="!isItemOwner(item) ? viewItem(item.item_id) : null"
      >
        <div class="item-icon">
          <img
            v-if="item.image_url"
            :src="`http://127.0.0.1:5000/api/items/uploads/${item.image_url.split(',')[0].trim()}`"
            alt="item"
            class="item-img"
          />
          <span v-else>{{ getItemIcon(item.category) }}</span>
        </div>
        <div class="item-info">
          <div class="item-name">{{ item.name }}</div>
          <div class="item-meta">📍 {{ item.location }} · {{ formatDate(item.date_reported) }}</div>
          <span class="item-badge" :class="getBadgeClass(item.report_type)">{{ item.report_type }}</span>
          <span v-if="item.status === 'Claimed'" class="item-badge badge-claimed">Claimed</span>
          <div v-if="!isItemOwner(item)" class="view-hint">👆 Click to view details</div>
        </div>
        <div class="item-actions" @click.stop>
          <button v-if="isItemOwner(item)" class="action-btn edit" @click="startEdit(item)" title="Edit">✏️</button>
          <button v-if="isItemOwner(item)" class="action-btn delete" @click="deleteItem(item.item_id)" title="Delete">🗑️</button>
          <button v-if="item.status !== 'Claimed' && isItemOwner(item)" class="action-btn claim" @click="markClaimed(item.item_id)" title="Mark as Claimed">✓</button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredItems.length === 0" class="empty-state">
      <div class="empty-icon">🔍</div>
      <h3>No items found</h3>
      <p>Try adjusting your filters or report a new item</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const items = ref([])
const filteredItems = ref([])
const editingId = ref(null)
const showForm = ref(false)
const fileInputKey = ref(0) // used to reset file input

// Filters
const searchQuery = ref('')
const filterCategory = ref('')
const filterStatus = ref('')
const filterLocation = ref('')

// Images
const selectedFiles = ref([])

const onFileSelected = (event) => {
  selectedFiles.value = Array.from(event.target.files).slice(0, 5)
}

const getPreviewUrl = (file) => URL.createObjectURL(file)

const removeSelectedFile = (index) => {
  selectedFiles.value = selectedFiles.value.filter((_, i) => i !== index)
}

const token = localStorage.getItem('token')
const currentUserId = localStorage.getItem('user_id')
const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }

const form = ref({
  name: '',
  category: '',
  report_type: 'Lost',
  location: '',
  floor: 'Ground Floor',
  date_reported: '',
  contact_info: '',
  description: '',
  existingImages: []
})

async function fetchItems() {
  const res = await axios.get('http://127.0.0.1:5000/api/items/')
  items.value = res.data
  applyFilters()
}

function applyFilters() {
  let result = items.value
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(item =>
      item.name.toLowerCase().includes(query) ||
      item.location.toLowerCase().includes(query) ||
      item.description?.toLowerCase().includes(query)
    )
  }
  if (filterCategory.value) result = result.filter(item => item.category === filterCategory.value)
  if (filterStatus.value) result = result.filter(item => item.report_type === filterStatus.value)
  if (filterLocation.value) result = result.filter(item => item.location.includes(filterLocation.value))
  filteredItems.value = result
}

function isItemOwner(item) {
  return String(item.user_id) === String(currentUserId || '')
}

function viewItem(id) {
  router.push(`/items/${id}`)
}

async function createItem() {
  if (!form.value.name || !form.value.category || !form.value.location || !form.value.date_reported) {
    alert('Please fill in all required fields (*).')
    return
  }
  try {
    const fd = new FormData()
    fd.append('name', form.value.name)
    fd.append('category', form.value.category)
    fd.append('report_type', form.value.report_type)
    fd.append('location', form.value.location)
    fd.append('floor', form.value.floor)
    fd.append('date_reported', form.value.date_reported)
    fd.append('description', form.value.description)
    fd.append('contact_info', form.value.contact_info)
    selectedFiles.value.forEach(file => fd.append('images', file))

    const currentToken = localStorage.getItem('token')
    await axios.post('http://127.0.0.1:5000/api/items/', fd, {
      headers: { Authorization: `Bearer ${currentToken}` }
    })
    resetForm()
    showForm.value = false
    fetchItems()
  } catch (err) {
    alert('Failed to create item. Make sure you are logged in.')
  }
}

async function updateItem() {
  try {
    const fd = new FormData()
    fd.append('name', form.value.name)
    fd.append('category', form.value.category)
    fd.append('report_type', form.value.report_type)
    fd.append('location', form.value.location)
    fd.append('floor', form.value.floor || 'Ground Floor')
    fd.append('date_reported', form.value.date_reported)
    fd.append('description', form.value.description || '')
    fd.append('contact_info', form.value.contact_info || '')
    selectedFiles.value.forEach(file => fd.append('images', file))

    const currentToken = localStorage.getItem('token')
    await axios.put(`http://127.0.0.1:5000/api/items/${editingId.value}`, fd, {
      headers: { Authorization: `Bearer ${currentToken}` }
    })
    resetForm()
    showForm.value = false
    fetchItems()
  } catch {
    alert('Failed to update item.')
  }
}

async function deleteItem(id) {
  if (confirm('Are you sure you want to delete this report?')) {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/items/${id}`, { headers })
      fetchItems()
    } catch {
      alert('Failed to delete item.')
    }
  }
}

async function markClaimed(id) {
  try {
    await axios.patch(`http://127.0.0.1:5000/api/items/${id}/status`, { status: 'Claimed' }, { headers })
    fetchItems()
  } catch {
    alert('Failed to update status.')
  }
}

function startEdit(item) {
  editingId.value = item.item_id
  form.value = {
    name: item.name,
    category: item.category,
    report_type: item.report_type,
    location: item.location,
    floor: item.floor || 'Ground Floor',
    date_reported: item.date_reported,
    description: item.description || '',
    contact_info: item.contact_info || '',
    existingImages: item.image_url ? item.image_url.split(',').map(s => s.trim()) : []
  }
  selectedFiles.value = []
  fileInputKey.value++  // resets the file input element
  showForm.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function cancelEdit() {
  editingId.value = null
  showForm.value = false
  resetForm()
}

function resetForm() {
  editingId.value = null
  form.value = {
    name: '',
    category: '',
    report_type: 'Lost',
    location: '',
    floor: 'Ground Floor',
    date_reported: '',
    contact_info: '',
    description: '',
    existingImages: []
  }
  selectedFiles.value = []
  fileInputKey.value++
}

function getItemIcon(category) {
  const icons = {
    'Electronics': '📱',
    'ID/Cards': '🆔',
    'Clothing': '👕',
    'Accessories': '🎒',
    'Books': '📖',
    'Keys': '🔑',
    'Other': '📦'
  }
  return icons[category] || '📦'
}

function getBadgeClass(reportType) {
  return reportType === 'Lost' ? 'badge-lost' : 'badge-found'
}

function formatDate(dateStr) {
  if (!dateStr) return 'Unknown date'
  const date = new Date(dateStr)
  const now = new Date()
  const diffDays = Math.ceil(Math.abs(now - date) / (1000 * 60 * 60 * 24))
  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  return date.toLocaleDateString()
}

onMounted(fetchItems)
</script>

<style scoped>
.items-page {
  min-height: 100vh;
  background: var(--background);
}

.filter-toolbar {
  padding: 18px 32px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 22px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.search-input {
  flex: 1;
  min-width: 250px;
  padding: 10px 14px;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #5c6bc0;
}

.filter-select {
  padding: 10px 12px;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 13px;
  background: #fff;
  color: #444;
  cursor: pointer;
}

.btn-add {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--primary);
  color: #fff;
  text-decoration: none;
  border: none;
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}

.btn-add:hover {
  background: var(--primary-strong);
  transform: translateY(-1px);
}

.report-form-container {
  background: #fff;
  padding: 28px 32px;
  margin: 24px 0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.report-form-container h3 {
  font-size: 18px;
  color: #1a237e;
  margin-bottom: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 12px;
  font-weight: 700;
  color: #888;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  color: #444;
  background: #fafafa;
  box-sizing: border-box;
}

.form-textarea {
  min-height: 80px;
  resize: vertical;
  font-family: inherit;
}

/* Image Preview */
.image-preview-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 10px;
  align-items: flex-start;
}

.preview-thumb {
  position: relative;
}

.thumb-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  border: 1.5px solid #ddd;
  display: block;
}

.thumb-remove {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #e53935;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 10px;
  cursor: pointer;
  line-height: 18px;
  text-align: center;
  padding: 0;
}

.preview-hint {
  width: 100%;
  font-size: 11px;
  color: #888;
  margin: 0;
}

.form-buttons {
  display: flex;
  gap: 12px;
}

.btn-submit {
  background: #1a237e;
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-submit:hover { background: #0d47a1; }

.btn-cancel {
  background: #757575;
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
  padding: 24px 0;
}

.item-card {
  background: var(--surface);
  border-radius: 18px;
  border: 1px solid var(--border);
  overflow: hidden;
  box-shadow: 0 16px 42px rgba(15, 23, 42, 0.08);
  transition: transform 0.25s, box-shadow 0.25s;
  position: relative;
}

.item-card.clickable { cursor: pointer; }

.item-card.clickable:hover {
  box-shadow: 0 8px 24px rgba(92, 107, 192, 0.2);
  transform: translateY(-3px);
  border-color: #5c6bc0;
}

.item-card:not(.clickable):hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  transform: translateY(-2px);
}

.item-icon {
  height: 120px;
  background: #e8eaf6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  overflow: hidden;
}

.item-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-info { padding: 14px; }

.item-name {
  font-size: 14px;
  font-weight: 700;
  color: #222;
  margin-bottom: 6px;
}

.item-meta {
  font-size: 11px;
  color: #888;
  margin-bottom: 10px;
}

.item-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-right: 6px;
}

.badge-lost { background: #fce4ec; color: #c62828; }
.badge-found { background: #e8f5e9; color: #2e7d32; }
.badge-claimed { background: #fffde7; color: #f57f17; }

.view-hint {
  font-size: 11px;
  color: #5c6bc0;
  margin-top: 8px;
  font-style: italic;
}

.item-actions {
  display: flex;
  gap: 6px;
  padding: 10px 14px;
  background: #f9f9f9;
  border-top: 1px solid #eee;
}

.action-btn {
  flex: 1;
  padding: 6px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn.edit { background: #e8eaf6; }
.action-btn.edit:hover { background: #c5cae9; }
.action-btn.delete { background: #ffebee; }
.action-btn.delete:hover { background: #ffcdd2; }
.action-btn.claim { background: #e8f5e9; }
.action-btn.claim:hover { background: #c8e6c9; }

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #888;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 18px;
  color: #666;
  margin-bottom: 8px;
}

.empty-state p { font-size: 14px; }

@media (max-width: 768px) {
  .filter-toolbar { padding: 12px 16px; }
  .items-grid { grid-template-columns: 1fr; padding: 16px 0; }
  .form-grid { grid-template-columns: 1fr; }
}
</style>