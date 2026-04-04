<template>
  <div class="auth-container">
    <div class="tabs">
      <button @click="mode = 'login'" :class="{ active: mode === 'login' }">Login</button>
      <button @click="mode = 'register'" :class="{ active: mode === 'register' }">Register</button>
    </div>

    <div v-if="mode === 'login'">
      <input v-model="email" placeholder="Email Address" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="login">Login to my Account</button>
    </div>

    <div v-else>
      <input v-model="studentId" placeholder="Student ID" />
      <input v-model="fullname" placeholder="Full Name" />
      <input v-model="email" placeholder="Email Address" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="register">Register</button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const mode = ref('login')
const email = ref('')
const password = ref('')
const fullname = ref('')
const studentId = ref('')
const error = ref('')

async function login() {
  try {
    const res = await axios.post('http://127.0.0.1:5000/api/auth/login', {
      email: email.value,
      password: password.value
    })
    localStorage.setItem('token', res.data.access_token)
    localStorage.setItem('fullname', res.data.fullname)
    router.push('/items')
  } catch {
    error.value = 'Invalid email or password.'
  }
}

async function register() {
  try {
    await axios.post('http://127.0.0.1:5000/api/auth/register', {
      student_id: studentId.value,
      full_name: fullname.value,
      email: email.value,
      password: password.value
    })
    error.value = ''
    mode.value = 'login'
    alert('Registered successfully! Please login.')
  } catch {
    error.value = 'Registration failed. Check your inputs.'
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 30px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 8px 16px;
  background-color: #1a73e8;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.active {
  background-color: #0d47a1;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>