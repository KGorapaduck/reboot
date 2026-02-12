<template>
  <div class="auth-container">
    <!-- Home Link Logo -->
    <router-link to="/" class="home-logo">RE BOOT</router-link>

    <div class="glass-container auth-box">
      <h2 style="text-align: center; margin-bottom: 25px; font-weight: 700;">환영합니다</h2>
      
      <!-- Student/Instructor Toggle (Already above inputs) -->
      <div class="tabs">
        <button 
          :class="['tab-btn', { active: userType === 'STUDENT' }]" 
          @click="userType = 'STUDENT'"
        >
          수강생
        </button>
        <button 
          :class="['tab-btn', { active: userType === 'INSTRUCTOR' }]" 
          @click="userType = 'INSTRUCTOR'"
        >
          강사
        </button>
      </div>

      <form @submit.prevent="handleLogin" style="display: flex; flex-direction: column; gap: 20px;">
        <div>
          <label style="display: block; margin-bottom: 8px; font-size: 0.9rem; font-weight: 500;">아이디</label>
          <input v-model="username" type="text" class="glass-input" placeholder="아이디를 입력하세요" required />
        </div>
        
        <div>
          <label style="display: block; margin-bottom: 8px; font-size: 0.9rem; font-weight: 500;">비밀번호</label>
          <input 
            v-model="password" 
            type="password" 
            class="glass-input" 
            placeholder="비밀번호를 입력하세요" 
            required 
            @keyup.enter="handleLogin"
          />
        </div>
      </form>

      <div class="button-group">
        <button @click="handleLogin" class="glass-button primary-btn">
          로그인
        </button>
        <button @click="router.push('/')" class="glass-button secondary-btn">
          뒤로가기
        </button>
      </div>
      
      <p style="text-align: center; margin-top: 25px; font-size: 0.9rem;">
        계정이 없으신가요? <router-link to="/signup" style="color: #fff; text-decoration: underline;">회원가입</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userType = ref('STUDENT')
const username = ref('')
const password = ref('')

const handleLogin = () => {
  // TODO: Implement actual API login
  console.log(`Logging in as ${userType.value} with ${username.value}`)
  
  // Mock login success
  localStorage.setItem('user_role', userType.value)
  localStorage.setItem('auth_token', 'mock_token')
  
  if (userType.value === 'INSTRUCTOR') {
    router.push('/instructor')
  } else {
    router.push('/dashboard')
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  position: relative;
}

.home-logo {
  position: absolute;
  top: 30px;
  left: 40px;
  font-size: 1.5rem;
  font-weight: 900;
  text-decoration: none;
  color: white;
  letter-spacing: 2px;
  z-index: 10;
  transition: opacity 0.3s;
}

.home-logo:hover {
  opacity: 0.8;
  text-shadow: 0 0 10px rgba(255,255,255,0.5);
}

.auth-box {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.tabs {
  display: flex;
  margin-bottom: 30px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 5px;
}

.tab-btn {
  flex: 1;
  padding: 10px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-weight: 600;
}

.tab-btn.active {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.glass-input {
  width: 100%;
  padding: 12px 15px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s;
}

.glass-input:focus {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 10px rgba(255,255,255,0.1);
}

.primary-btn {
  flex: 1; /* Equal width */
  padding: 12px;
  background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 100%);
  border: 1px solid rgba(255,255,255,0.4);
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 10px;
  cursor: pointer;
}

.primary-btn:hover {
  background: linear-gradient(135deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0.2) 100%);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.secondary-btn {
  flex: 1; /* Equal width */
  padding: 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 10px;
  color: #ddd;
  cursor: pointer;
  transition: all 0.3s;
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  transform: translateY(-2px);
}

.button-group {
  display: flex;
  gap: 15px;
  margin-top: 20px;
  width: 100%;
}
</style>
