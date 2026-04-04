<template>
  <div class="container">
    <div class="header">
      <h2>Campus Lost & Found</h2>
      <button @click="logout" class="logout-btn">Logout</button>
    </div>

    <!-- Form -->
    <div class="form">
      <h3>{{ editingId ? 'Edit Report' : 'Submit New Report' }}</h3>
      <input v-model="form.name" placeholder="Item Name" />
      <input v-model="form.category" placeholder="Category (e.g. Electronics, ID, Clothing)" />
      <select v-model="form.report_type">
        <option>Lost</option>
        <option>Found</option>
      </select>
      <input v-model="form.location" placeholder="Location" />
      <input v-model="form.date_reported" type="date" />
      <input v-model="form.contact_info" placeholder="Contact Info" />
      <textarea v-model="form.description" placeholder="Description"></textarea>
      <div class="form-buttons">
        <button @click="editingId ? updateItem() : createItem()">
          {{ editingId ? 'Update Item' : 'Submit Report' }}
        </button>
        <button v-if="editingId" @click="cancelEdit" class="cancel-btn">Cancel</button>
      </div>
    </div>

    <!-- Items Table -->
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Category</th>
          <th>Type</th>
          <th>Status</th>
          <th>Location</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.item_id">
          <td>{{ item.name }}</td>
          <td>{{ item.category }}</td>
          <td>{{ item.report_type }}</td>
          <td>{{ item.status }}</td>
          <td>{{ item.location }}</td>
          <td>
            <button @click="startEdit(item)" class="edit-btn">Edit</button>
            <button @click="deleteItem(item.item_id)" class="delete-btn">Delete</button>
            <button @click="markClaimed(item.item_id)" class="claim-btn">Mark Claimed</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const items = ref([])
const editingId = ref(null)
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
}

async function createItem() {
  try {
    const currentToken = localStorage.getItem('token')
    const currentHeaders = { 
      Authorization: `Bearer ${currentToken}`,
      'Content-Type': 'application/json'
    }
    await axios.post('http://127.0.0.1:5000/api/items/', form.value, { headers: currentHeaders })
    resetForm()
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
  localStorage.removeItem('token')
  localStorage.removeItem('fullname')
  router.push('/')
}

onMounted(fetchItems)
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 30px auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.form {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 30px;
}

.form input, .form select, .form textarea {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-buttons {
  display: flex;
  gap: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #1a73e8;
  color: white;
}

button {
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
  background-color: #1a73e8;
}

.edit-btn { background-color: #f9a825; }
.delete-btn { background-color: #e53935; }
.claim-btn { background-color: #43a047; }
.cancel-btn { background-color: #757575; }
.logout-btn { background-color: #e53935; }
</style>