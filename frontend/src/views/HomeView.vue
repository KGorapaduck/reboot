<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

const router = useRouter()
const isLoggedIn = ref(false)
const userRole = ref(null)

const checkLoginStatus = () => {
  const token = localStorage.getItem('auth_token')
  isLoggedIn.value = !!token
  if (token) {
    userRole.value = localStorage.getItem('user_role')
  } else {
    userRole.value = null
  }
}

const logout = () => {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('user_role')
  isLoggedIn.value = false
  userRole.value = null
  alert('로그아웃 되었습니다.')
}

const navigateTo = (path) => {
  if (isLoggedIn.value) {
    router.push(path)
  } else {
    router.push('/login')
  }
}

onMounted(() => {
  checkLoginStatus()
})
</script>

<template>
  <div class="home-container">
    <!-- Custom Header for Landing Page -->
    <header class="landing-header">
      <div class="header-left">
        <template v-if="isLoggedIn">
          <template v-if="userRole === 'STUDENT'">
            <a @click="navigateTo('/dashboard')" class="nav-item">대시보드</a>
            <a @click="navigateTo('/classroom')" class="nav-item">강의실</a>
          </template>
          <template v-if="userRole === 'INSTRUCTOR'">
            <a @click="navigateTo('/instructor')" class="nav-item">강사 페이지</a>
          </template>
        </template>
      </div>
      <div class="header-right">
        <button v-if="isLoggedIn" @click="logout" class="glass-button login-btn">로그아웃</button>
        <router-link v-else to="/login" class="glass-button login-btn">로그인</router-link>
      </div>
    </header>

    <!-- Main Content: Full-width Glass Panel -->
    <div class="glass-container hero-panel">
      <h1 class="main-logo">RE BOOT</h1>
      <p class="sub-text">New start to your career</p>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  height: 100vh; /* Fixed height to viewport */
  width: 100vw;
  overflow: hidden; /* Prevent scrolling */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  background: #6360eff7; /* Fallback background */
}

.landing-header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  padding: 25px 30px; /* Increased padding for better spacing */
  display: flex;
  justify-content: center; /* Center the nav items if present */
  align-items: center;
  z-index: 10;
  box-sizing: border-box; /* Ensure padding doesn't affect width */
}

/* Position login button strictly via absolute positioning */
.header-right {
  position: absolute;
  right: 30px;
  top: 25px;
}

.header-left {
  display: flex;
  gap: 30px;
}

.nav-item {
  font-size: 1.2rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.85); /* Slightly brighter */
  cursor: pointer;
  transition: color 0.3s;
  text-decoration: none;
}

.nav-item:hover {
  color: #fff;
  text-shadow: 0 0 10px rgba(255,255,255,0.7);
}

.login-btn {
  padding: 10px 30px; /* Larger click area */
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(124, 173, 174, 0.5);
  color: white;
  text-decoration: none;
  border-radius: 30px;
  font-weight: 600;
  transition: all 0.3s;
  backdrop-filter: blur(50px);
}

.login-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.421);
}

.hero-panel {
  padding: 10px;
  width: 100%; /* Adjusted from 90% */
  height: 75vh; /* Adjusted from 85vh */
  max-width: 8000px; /* Optional: limit max width for very large screens */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  border-radius: 24px;
  
  /* Glassmorphism overrides */
  background: url('/logo.png') no-repeat center center;
  background-size: auto; /* Ensures image covers the entire panel */
  /* Add overlay to ensure text readability */
  position: relative;
  z-index: 1;
  border: 0px;
  overflow: hidden;
}

.hero-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3); /* Slightly lighter overlay */
  border-radius: 24px;
  z-index: -1;
  backdrop-filter: blur(2px); /* Reduced blur */
  border: 0px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  display: block;
  width:150%;
  height: 150%;
}

.main-logo {
  font-size: 8rem; /* Very Large Text */
  font-weight: 900;
  letter-spacing: 10px;
  line-height: 1;
  margin: 0;
  
  /* Increased transparency for "duck visibility" */
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.5) 0%, rgba(168, 192, 255, 0.5) 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  
  filter: drop-shadow(0 0 20px rgba(168, 192, 255, 0.3));
}

.sub-text {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 20px;
  letter-spacing: 2px;
}
</style>
