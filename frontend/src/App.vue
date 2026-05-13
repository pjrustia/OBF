<template>
  <div class="page-shell">
    <div class="top-nav">
      <div class="brand">One Big Find</div>
      <div class="nav-items" v-if="isLoggedIn">
        <router-link to="/items" class="nav-link" exact-active-class="active">Item List</router-link>
        <router-link to="/report" class="nav-link" exact-active-class="active">Report Item</router-link>
        <router-link to="/dashboard" class="nav-link" exact-active-class="active">My Reports</router-link>
      </div>
      <div class="nav-actions">
        <span v-if="isLoggedIn" class="user-name">👤 {{ userName }}</span>
        <button v-if="isLoggedIn" class="btn-secondary" @click="logout">Logout</button>
        <router-link v-else to="/" class="btn-primary">Login</router-link>
      </div>
    </div>

    <div class="page-content">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const userName = ref(localStorage.getItem('fullname') || '')
const isLoggedIn = ref(Boolean(localStorage.getItem('token')))

watch(
  () => route.fullPath,
  () => {
    userName.value = localStorage.getItem('fullname') || ''
    isLoggedIn.value = Boolean(localStorage.getItem('token'))
  }
)

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('fullname')
  localStorage.removeItem('user_id')
  userName.value = ''
  isLoggedIn.value = false
  router.push('/')
}
</script>

<style>
:root {
  --background: #eef2ff;
  --surface: #ffffff;
  --surface-soft: #f8f9ff;
  --primary: #1a237e;
  --primary-soft: #3949ab;
  --accent: #5563c1;
  --text: #111827;
  --muted: #6b7280;
  --border: #e2e8f0;
  --primary-strong: #0d47a1;
  --shadow: rgba(21, 40, 80, 0.08);
}

* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
  min-height: 100%;
  background: var(--background);
  color: var(--text);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

button,
input,
select,
textarea {
  font-family: inherit;
}

.page-shell {
  min-height: 100vh;
  background: linear-gradient(180deg, var(--background) 0%, #f7f9ff 100%);
}

.top-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 16px 32px;
  background: linear-gradient(90deg, var(--primary), var(--primary-soft));
  color: #fff;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.14);
}

.brand {
  font-weight: 800;
  letter-spacing: 0.12em;
  font-size: 1rem;
}

.nav-items {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 18px;
  border-radius: 999px;
  color: rgba(255,255,255,0.9);
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s, color 0.2s;
}

.nav-link:hover,
.nav-link.active,
.nav-link.router-link-active {
  background: rgba(255,255,255,0.18);
  color: #fff;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-name {
  font-weight: 700;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 22px;
  border: none;
  border-radius: 999px;
  background: var(--primary);
  color: #fff;
  cursor: pointer;
  font-weight: 700;
  text-decoration: none;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 22px;
  border: none;
  border-radius: 999px;
  background: #eef2ff;
  color: var(--text);
  cursor: pointer;
  font-weight: 700;
  text-decoration: none;
}

.page-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 28px 32px 48px;
}

.page-card {
  background: var(--surface);
  border-radius: 28px;
  box-shadow: 0 24px 60px rgba(21, 40, 80, 0.08);
  padding: 28px;
}

.form-input,
.form-textarea,
select {
  font-family: inherit;
}
</style>