<template>
  <div class="items-page">
    <!-- Top Navigation -->
    <div class="top-nav">
      <div class="logo">🔍 One Big Find</div>
      <div class="nav-items">
        <span class="nav-link active">Browse Items</span>
        <span class="nav-link">My Reports</span>
      </div>
      <div class="user-chip" @click="logout">
        👤 {{ userName }} &nbsp;▾
      </div>
    </div>

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
        <option>Main Library</option>
        <option>Gym</option>
        <option>Cafeteria</option>
        <option>Computer Lab</option>
        <option>Parking Lot</option>
      </select>
      <button class="btn-add" @click="showForm = !showForm">
        {{ showForm ? '✕ Close Form' : '+ Report Item' }}
      </button>
    </div>

    <!-- Report Form (Toggle) -->
    <div v-if="showForm" class="report-form-container">
      <h3>{{ editingId ? '✏️ Edit Report' : '📋 Report a Lost or Found Item' }}</h3>
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
          <label>Report Type *</label>
          <select v-model="form.report_type" class="form-input">
            <option>Lost</option>
            <option>Found</option>
          </select>
        </div>
        <div class="form-group">
          <label>Date Lost/Found *</label>
          <input v-model="form.date_reported" type="date" class="form-input" />
        </div>
        <div class="form-group full-width">
          <label>Last Seen / Found Location *</label>
          <input v-model="form.location" class="form-input" placeholder="e.g. Main Library, 2nd Floor near exit" />
        </div>
        <div class="form-group full-width">
          <label>Description</label>
          <textarea v-model="form.description" class="form-textarea" placeholder="Describe the item — color, size, brand, distinguishing marks..."></textarea>
        </div>
        <div class="form-group full-width">
          <label>Contact Info</label>
          <input v-model="form.contact_info" class="form-input" placeholder="Phone or alternate email (visible only to matched user)" />
        </div>
      </div>
      <div class="form-buttons">
        <button class="btn-submit" @click="editingId ? updateItem() : createItem()">
          {{ editingId ? 'Update Report' : 'Submit Report' }}
        </button>
        <button v-if="editingId" class="btn-cancel" @click="cancelEdit">Cancel</button>
      </div>
    </div>

    <!-- Items Grid -->
    <div class="items-grid">
      <div v-for="item in filteredItems" :key="item.item_id" class="item-card">
        <div class="item-icon">
          {{ getItemIcon(item.category) }}
        </div>
        <div class="item-info">
          <div class="item-name">{{ item.name }}</div>
          <div class="item-meta">📍 {{ item.location }} · {{ formatDate(item.date_reported) }}</div>
          <span class="item-badge" :class="getBadgeClass(item.report_type)">
            {{ item.report_type }}
          </span>
          <span v-if="item.status === 'Claimed'" class="item-badge badge-claimed">Claimed</span>
        </div>
        <div class="item-actions">
          <button class="action-btn edit" @click="startEdit(item)" title="Edit">✏️</button>
          <button class="action-btn delete" @click="deleteItem(item.item_id)" title="Delete">🗑️</button>
          <button v-if="item.status !== 'Claimed'" class="action-btn claim" @click="markClaimed(item.item_id)" title="Mark as Claimed">✓</button>
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
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const items = ref([])
const filteredItems = ref([])
const editingId = ref(null)
const showForm = ref(false)
const userName = ref(localStorage.getItem('fullname') || 'User')

// Filters
const searchQuery = ref('')
const filterCategory = ref('')
const filterStatus = ref('')
const filterLocation = ref('')

const token = localStorage.getItem('token')
const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }

const form = ref({
  name: '',
  category: '',
  report_type: 'Lost',
  location: '',
  date_reported: '',
  contact_info: '',
  description: ''
})

async function fetchItems() {
  const res = await axios.get('http://127.0.0.1:5000/api/items/')
  items.value = res.data
  applyFilters()
}

function applyFilters() {
  let result = items.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(item => 
      item.name.toLowerCase().includes(query) || 
      item.location.toLowerCase().includes(query) ||
      item.description?.toLowerCase().includes(query)
    )
  }

  // Category filter
  if (filterCategory.value) {
    result = result.filter(item => item.category === filterCategory.value)
  }

  // Status filter
  if (filterStatus.value) {
    result = result.filter(item => item.report_type === filterStatus.value)
  }

  // Location filter
  if (filterLocation.value) {
    result = result.filter(item => item.location.includes(filterLocation.value))
  }

  filteredItems.value = result
}

async function createItem() {
  if (!form.value.name || !form.value.category || !form.value.location || !form.value.date_reported) {
    alert('Please fill in all required fields (*).')
    return
  }

  try {
    const currentToken = localStorage.getItem('token')
    const currentHeaders = { 
      Authorization: `Bearer ${currentToken}`,
      'Content-Type': 'application/json'
    }
    await axios.post('http://127.0.0.1:5000/api/items/', form.value, { headers: currentHeaders })
    resetForm()
    showForm.value = false
    fetchItems()
  } catch (err) {
    console.log(err)
    alert('Failed to create item. Make sure you are logged in.')
  }
}

async function updateItem() {
  try {
    await axios.put(`http://127.0.0.1:5000/api/items/${editingId.value}`, form.value, { headers })
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
  form.value = { ...item }
  showForm.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function cancelEdit() {
  editingId.value = null
  resetForm()
}

function resetForm() {
  editingId.value = null
  form.value = {
    name: '',
    category: '',
    report_type: 'Lost',
    location: '',
    date_reported: '',
    contact_info: '',
    description: ''
  }
}

function logout() {
  if (confirm('Are you sure you want to logout?')) {
    localStorage.removeItem('token')
    localStorage.removeItem('fullname')
    router.push('/')
  }
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
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
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
  background: #f0f2f5;
}

/* Top Navigation */
.top-nav {
  background: #1a237e;
  color: #fff;
  padding: 14px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.logo {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.nav-items {
  display: flex;
  gap: 24px;
  font-size: 14px;
}

.nav-link {
  opacity: 0.75;
  cursor: pointer;
  transition: opacity 0.3s;
}

.nav-link:hover,
.nav-link.active {
  opacity: 1;
  font-weight: 600;
}

.user-chip {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.user-chip:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* Filter Toolbar */
.filter-toolbar {
  padding: 18px 32px;
  background: #fff;
  border-bottom: 1px solid #e0e0e0;
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
  background: #3949ab;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-add:hover {
  background: #1a237e;
}

/* Report Form */
.report-form-container {
  background: #fff;
  padding: 28px 32px;
  margin: 24px 32px;
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

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  display: block;
  font-size: 12px;
  font-weight: 700;
  color: #888;
  margin-bottom: 6px;
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
}

.form-textarea {
  min-height: 80px;
  resize: vertical;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #5c6bc0;
  background: #fff;
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

.btn-submit:hover {
  background: #0d47a1;
}

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

/* Items Grid */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
  padding: 24px 32px;
}

.item-card {
  background: #fff;
  border-radius: 12px;
  border: 1.5px solid #e8eaf6;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: all 0.3s;
  position: relative;
}

.item-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  transform: translateY(-2px);
}

.item-icon {
  height: 100px;
  background: #e8eaf6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
}

.item-info {
  padding: 14px;
}

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

.badge-lost {
  background: #fce4ec;
  color: #c62828;
}

.badge-found {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge-claimed {
  background: #fffde7;
  color: #f57f17;
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

.action-btn.edit {
  background: #e8eaf6;
}

.action-btn.edit:hover {
  background: #c5cae9;
}

.action-btn.delete {
  background: #ffebee;
}

.action-btn.delete:hover {
  background: #ffcdd2;
}

.action-btn.claim {
  background: #e8f5e9;
}

.action-btn.claim:hover {
  background: #c8e6c9;
}

/* Empty State */
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

.empty-state p {
  font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  .filter-toolbar {
    padding: 12px 16px;
  }
  
  .items-grid {
    grid-template-columns: 1fr;
    padding: 16px;
  }
  
  .report-form-container {
    margin: 16px;
    padding: 20px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
