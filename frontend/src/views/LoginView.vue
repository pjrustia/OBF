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
            <button class="btn-primary full-width" @click="login">Login to my Account</button>
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
            <button class="btn-primary full-width" @click="register">Create Account</button>
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
    localStorage.setItem('user_id', res.data.user_id)
    error.value = ''
    router.push('/dashboard')
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
  min-height: calc(100vh - 98px);
  gap: 24px;
  align-items: center;
  justify-content: center;
}

/* Left Panel - Branding */
.auth-left {
  flex: 1.05;
  min-height: 520px;
  border-radius: 32px;
  background: linear-gradient(145deg, var(--primary), var(--primary-soft));
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 48px 36px;
  color: #fff;
  text-align: center;
  box-shadow: 0 30px 90px rgba(15, 23, 42, 0.18);
}

.brand-icon {
  width: 90px;
  height: 90px;
  background: rgba(255, 255, 255, 0.16);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 42px;
  margin-bottom: 30px;
}

.auth-left h2 {
  font-size: 34px;
  font-weight: 800;
  margin-bottom: 16px;
}

.auth-left p {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 12px;
}

.tagline {
  font-size: 15px;
  opacity: 0.8;
  line-height: 1.8;
  max-width: 420px;
}

/* Right Panel - Form */
.auth-right {
  flex: 0.85;
  background: var(--surface);
  border-radius: 32px;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.12);
  padding: 42px;
}

/* Tab Toggle */
.tab-row {
  display: flex;
  border-bottom: 1px solid var(--border);
  margin-bottom: 32px;
}

.tab-btn {
  flex: 1;
  padding: 14px;
  text-align: center;
  font-size: 15px;
  font-weight: 600;
  color: var(--muted);
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: all 0.3s;
}

.tab-btn:hover {
  color: var(--primary);
}

.tab-btn.active {
  color: var(--primary);
  border-bottom: 3px solid var(--primary);
}

/* Form Elements */
.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  font-size: 12px;
  font-weight: 700;
  color: var(--muted);
  margin-bottom: 8px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 1.5px solid var(--border);
  border-radius: 14px;
  font-size: 14px;
  color: var(--text);
  background: #f8f9ff;
  transition: all 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary);
  background: #fff;
}

.btn-primary.full-width {
  width: 100%;
}

.btn-link {
  text-align: center;
  font-size: 13px;
  color: var(--muted);
  margin-top: 18px;
}

.btn-link span {
  color: var(--primary);
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
  border-radius: 8px;
}

/* Responsive */
@media (max-width: 980px) {
  .auth-wrap {
    flex-direction: column;
    min-height: auto;
  }
  
  .auth-left,
  .auth-right {
    width: 100%;
  }
  
  .auth-left {
    padding: 36px 28px;
  }
  
  .auth-right {
    padding: 36px 28px;
  }
}

@media (max-width: 640px) {
  .top-nav {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
