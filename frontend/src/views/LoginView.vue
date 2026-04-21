<template>
  <div class="auth-wrap">
    <!-- Left Panel - Branding -->
    <div class="auth-left">
      <div class="brand-icon">🔍</div>
      <h2>One Big Find</h2>
      <p>Campus Lost & Found Tracker</p>
      <p class="tagline">Reconnect students with their lost belongings. Post, search, and claim items right from your browser.</p>
    </div>

    <!-- Right Panel - Form -->
    <div class="auth-right">
      <!-- Tab Toggle -->
      <div class="tab-row">
        <div 
          class="tab-btn" 
          :class="{ active: mode === 'login' }" 
          @click="mode = 'login'"
        >
          🔐 Login
        </div>
        <div 
          class="tab-btn" 
          :class="{ active: mode === 'register' }" 
          @click="mode = 'register'"
        >
          📝 Register
        </div>
      </div>

      <!-- Login Form -->
      <div v-if="mode === 'login'">
        <div class="form-group">
          <label>Email Address</label>
          <input 
            v-model="email" 
            type="text" 
            class="form-input" 
            placeholder="e.g. juandelacruz@school.edu.ph"
          />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input 
            v-model="password" 
            type="password" 
            class="form-input" 
            placeholder="••••••••"
          />
        </div>
        <button class="btn-primary" @click="login">Login to my Account</button>
        <div class="btn-link">
          No account yet? <span @click="mode = 'register'">Register</span>
        </div>
      </div>

      <!-- Register Form -->
      <div v-else>
        <div class="form-group">
          <label>Full Name</label>
          <input 
            v-model="fullname" 
            class="form-input" 
            placeholder="e.g. Juan Dela Cruz"
          />
        </div>
        <div class="form-group">
          <label>Student ID</label>
          <input 
            v-model="studentId" 
            class="form-input" 
            placeholder="e.g. 2021-12345"
          />
        </div>
        <div class="form-group">
          <label>Email Address</label>
          <input 
            v-model="email" 
            type="text" 
            class="form-input" 
            placeholder="e.g. juandelacruz@school.edu.ph"
          />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input 
            v-model="password" 
            type="password" 
            class="form-input" 
            placeholder="••••••••"
          />
        </div>
        <button class="btn-primary" @click="register">Create Account</button>
        <div class="btn-link">
          Already have an account? <span @click="mode = 'login'">Login</span>
        </div>
      </div>

      <!-- Error Message -->
      <p v-if="error" class="error-msg">{{ error }}</p>
    </div>
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
    error.value = ''
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
.auth-wrap {
  display: flex;
  min-height: 100vh;
}

/* Left Panel - Branding */
.auth-left {
  flex: 1;
  background: linear-gradient(145deg, #1a237e, #3949ab);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  color: #fff;
  text-align: center;
}

.brand-icon {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.18);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  margin-bottom: 24px;
}

.auth-left h2 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
}

.auth-left p {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 8px;
}

.tagline {
  font-size: 14px;
  opacity: 0.75;
  line-height: 1.6;
  max-width: 400px;
}

/* Right Panel - Form */
.auth-right {
  flex: 1;
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: #fff;
}

/* Tab Toggle */
.tab-row {
  display: flex;
  border-bottom: 2px solid #e0e0e0;
  margin-bottom: 32px;
}

.tab-btn {
  flex: 1;
  padding: 12px;
  text-align: center;
  font-size: 15px;
  font-weight: 600;
  color: #999;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: all 0.3s;
}

.tab-btn:hover {
  color: #1a237e;
}

.tab-btn.active {
  color: #1a237e;
  border-bottom: 3px solid #1a237e;
}

/* Form Elements */
.form-group {
  margin-bottom: 18px;
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

.form-input {
  width: 100%;
  padding: 12px 14px;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  color: #444;
  background: #fafafa;
  transition: all 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #5c6bc0;
  background: #fff;
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background: #1a237e;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 12px;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #0d47a1;
}

.btn-link {
  text-align: center;
  font-size: 13px;
  color: #888;
  margin-top: 18px;
}

.btn-link span {
  color: #3949ab;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
}

.error-msg {
  color: #e53935;
  margin-top: 16px;
  font-size: 13px;
  text-align: center;
  background: #ffebee;
  padding: 10px;
  border-radius: 6px;
}

/* Responsive */
@media (max-width: 768px) {
  .auth-wrap {
    flex-direction: column;
  }
  
  .auth-left {
    padding: 30px 20px;
  }
  
  .auth-right {
    padding: 40px 30px;
  }
}
</style>
