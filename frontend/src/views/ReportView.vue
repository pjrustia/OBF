<template>
  <div class="report-page">
      <div class="page-card report-card">
        <div class="report-title">
          <h1>Report an Item</h1>
          <p>Submit a new lost or found item to the system.</p>
        </div>

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
            <label>Building Location *</label>
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
          <div class="form-group">
            <label>Floor Number *</label>
            <select v-model="form.floor" class="form-input">
              <option>Ground Floor</option>
              <option>2nd Floor</option>
              <option>3rd Floor</option>
              <option>4th Floor</option>
            </select>
          </div>
          <div class="form-group full-width">
            <label>Item Image *</label>
            <input type="file" @change="onFileSelected" class="form-input" accept="image/*" />
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

        <div class="form-actions">
          <button class="btn-primary" @click="submitReport">Submit Report</button>
        </div>
      </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const displayName = ref(localStorage.getItem('fullname') || 'User')
const showDropdown = ref(false)
const selectedFile = ref(null)

const form = ref({
  name: '',
  category: '',
  report_type: 'Lost',
  location: '',
  floor: 'Ground Floor',
  date_reported: '',
  contact_info: '',
  description: ''
})

const token = localStorage.getItem('token')

const onFileSelected = (event) => {
  selectedFile.value = event.target.files[0]
}

async function submitReport() {
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

    if (selectedFile.value) {
      fd.append('image', selectedFile.value)
    }

    await axios.post('http://127.0.0.1:5000/api/items/', fd, {
      headers: { Authorization: `Bearer ${token}` }
    })
    router.push('/dashboard')
  } catch (err) {
    console.error('Report submission error:', err.response?.data || err.message)
    alert('Failed to submit report. Please login again or try later.')
  }
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('fullname')
  localStorage.removeItem('user_id')
  router.push('/')
}
</script>

<style scoped>
.report-page {
  min-height: 100vh;
  color: var(--text);
}

.report-card {
  background: var(--surface);
  border-radius: 28px;
  padding: 32px;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
}

.report-title h1 {
  margin: 0;
  font-size: 32px;
}

.report-title p {
  margin: 10px 0 0;
  color: var(--muted);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
  margin-top: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.full-width {
  grid-column: 1 / -1;
}

.form-input,
.form-textarea,
select {
  width: 100%;
  padding: 14px 16px;
  border: 1.5px solid var(--border);
  border-radius: 14px;
  font-size: 14px;
  color: var(--text);
  background: #f8f9ff;
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

.form-actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 980px) {
  .page-content {
    padding: 24px 20px 36px;
  }

  .report-card {
    padding: 24px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>