<template>
  <div class="dashboard-page">
    <main class="dashboard-body">
      <header class="dashboard-header">
        <div>
          <p class="dashboard-label">One Big Find</p>
          <h1>Hello, {{ displayName }}!</h1>
          <p class="dashboard-subtitle">Here's a summary of your submitted reports.</p>
        </div>
      </header>

      <section class="summary-grid">
        <div class="summary-card">
          <span class="summary-label">LOST REPORTS</span>
          <strong>{{ lostReports }}</strong>
        </div>
        <div class="summary-card">
          <span class="summary-label">FOUND REPORTS</span>
          <strong>{{ foundReports }}</strong>
        </div>
        <div class="summary-card">
          <span class="summary-label">CLAIMED</span>
          <strong>{{ claimedReports }}</strong>
        </div>
        <div class="summary-card">
          <span class="summary-label">TOTAL POSTS</span>
          <strong>{{ totalReports }}</strong>
        </div>
      </section>

      <section class="reports-panel">
        <div class="reports-panel-header">
          <div>
            <h2>My Submitted Reports</h2>
            <p>Review and manage your uploaded items.</p>
          </div>
          <button class="btn-secondary" @click="goToReport">New Report</button>
        </div>

        <div class="reports-table-wrapper">
          <table class="reports-table">
            <thead>
              <tr>
                <th>ITEM NAME</th>
                <th>TYPE</th>
                <th>STATUS</th>
                <th>DATE</th>
                <th>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in items" :key="item.item_id">
                <td>{{ item.name }}</td>
                <td :class="item.report_type === 'Lost' ? 'status-lost' : 'status-found'">{{ item.report_type }}</td>
                <td :class="item.status === 'Claimed' ? 'status-claimed' : 'status-active'">{{ item.status }}</td>
                <td>{{ formatDate(item.date_reported) }}</td>
                <td class="actions-cell">
                  <button class="icon-btn edit" @click="editReport(item)">✏️</button>
                  <button class="icon-btn delete" @click="deleteReport(item.item_id)">🗑️</button>
                </td>
              </tr>
              <tr v-if="items.length === 0">
                <td colspan="5" class="empty-row">You have no submitted reports yet.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const items = ref([])
const displayName = ref(localStorage.getItem('fullname') || 'Ateneano')
const token = localStorage.getItem('token')
const headers = { Authorization: `Bearer ${token}` }

const lostReports = computed(() => items.value.filter((item) => item.report_type === 'Lost').length)
const foundReports = computed(() => items.value.filter((item) => item.report_type === 'Found').length)
const claimedReports = computed(() => items.value.filter((item) => item.status === 'Claimed').length)
const totalReports = computed(() => items.value.length)

async function fetchMyReports() {
  try {
    const res = await axios.get('http://127.0.0.1:5000/api/items/mine', { headers })
    items.value = res.data
  } catch (err) {
    console.error(err)
  }
}

async function deleteReport(id) {
  if (!confirm('Delete this report?')) return
  try {
    await axios.delete(`http://127.0.0.1:5000/api/items/${id}`, { headers })
    items.value = items.value.filter((item) => item.item_id !== id)
  } catch (err) {
    alert('Could not delete report.')
  }
}

function editReport(item) {
  router.push('/report')
}

function goToReport() {
  router.push('/report')
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('fullname')
  localStorage.removeItem('user_id')
  router.push('/')
}

function formatDate(dateStr) {
  if (!dateStr) return 'Unknown'
  const date = new Date(dateStr)
  return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}

onMounted(fetchMyReports)
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: var(--background);
}

.dashboard-body {
  max-width: 1200px;
  margin: 0 auto;
  padding: 28px 32px 48px;
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  gap: 24px;
}

.dashboard-label {
  margin: 0 0 10px;
  font-size: 14px;
  font-weight: 700;
  color: #4f5bbb;
}

.dashboard-header h1 {
  margin: 0;
  font-size: 32px;
}

.dashboard-subtitle {
  margin: 8px 0 0;
  color: #5f6f92;
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  gap: 24px;
}

.dashboard-label {
  margin: 0 0 10px;
  font-size: 14px;
  font-weight: 700;
  color: #4f5bbb;
}

.dashboard-header h1 {
  margin: 0;
  font-size: 32px;
}

.dashboard-subtitle {
  margin: 8px 0 0;
  color: #5f6f92;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
  margin-bottom: 30px;
}

.summary-card {
  background: var(--surface);
  border-radius: 20px;
  padding: 26px 20px;
  box-shadow: 0 18px 44px rgba(21, 40, 80, 0.08);
}

.summary-label {
  display: block;
  font-size: 12px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #6b78b5;
  margin-bottom: 10px;
}

.summary-card strong {
  font-size: 36px;
  color: #111827;
}

.reports-panel {
  background: var(--surface);
  border-radius: 30px;
  padding: 30px;
  box-shadow: 0 20px 45px rgba(21, 40, 80, 0.08);
}

.reports-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 22px;
}

.reports-panel-header h2 {
  margin: 0;
}

.reports-panel-header p {
  margin: 8px 0 0;
  color: #6b7280;
}

.reports-table-wrapper {
  overflow-x: auto;
}

.reports-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 780px;
}

.reports-table th,
.reports-table td {
  text-align: left;
  padding: 16px 18px;
}

.reports-table thead {
  background: #eef2ff;
}

.reports-table th {
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #4b5563;
}

.reports-table tbody tr {
  border-bottom: 1px solid #e6e8f0;
}

.reports-table tbody tr:last-child {
  border-bottom: none;
}

.reports-table td {
  color: #1f2937;
}

.status-lost {
  color: #d02f2f;
  font-weight: 700;
}

.status-found {
  color: #0f7f4e;
  font-weight: 700;
}

.status-claimed {
  color: #2563eb;
  font-weight: 700;
}

.status-active {
  color: #6b7280;
  font-weight: 700;
}

.actions-cell {
  display: flex;
  gap: 10px;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  background: #eef2ff;
  color: #1f2937;
}

.icon-btn.edit {
  background: #dbeafe;
}

.icon-btn.delete {
  background: #fee2e2;
}

.empty-row {
  text-align: center;
  padding: 28px 0;
  color: #6b7280;
}

.btn-primary,
.btn-secondary {
  padding: 12px 22px;
  border: none;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary {
  background: #2563eb;
  color: #fff;
}

.btn-secondary {
  background: #eef2ff;
  color: #1f2937;
}
</style>
