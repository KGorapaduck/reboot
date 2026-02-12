<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const userRole = ref(localStorage.getItem('user_role'))

// Update role when route changes (e.g. after login)
watch(route, () => {
  userRole.value = localStorage.getItem('user_role')
})

const showNavbar = computed(() => {
  // Hide navbar on landing, login, and signup pages
  return !['home', 'login', 'signup'].includes(route.name)
})

const handleLogout = () => {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('user_role')
  userRole.value = null
  alert('로그아웃 되었습니다.')
  router.push('/')
}
</script>

<template>
  <header v-if="showNavbar">
    <div class="wrapper glass-container" style="margin: 20px; display: flex; justify-content: space-between; align-items: center;">
      <!-- LEFT: Logo + Nav Links -->
      <div class="header-left">
        <div class="logo">
          <RouterLink to="/" style="text-decoration: none;">
            <h2 style="margin: 0; color: #fff; cursor: pointer;">Re:Boot</h2>
          </RouterLink>
        </div>

        <nav class="main-nav">
          <!-- Student Links -->
          <template v-if="userRole === 'STUDENT'">
            <RouterLink to="/dashboard" class="nav-link">대시보드</RouterLink>
            <RouterLink to="/classroom" class="nav-link">강의실</RouterLink>
            <RouterLink to="/mypage" class="nav-link">마이페이지</RouterLink>
          </template>

          <!-- Instructor Links -->
          <template v-if="userRole === 'INSTRUCTOR'">
            <RouterLink to="/instructor" class="nav-link">강사 페이지</RouterLink>
          </template>
        </nav>
      </div>

      <!-- RIGHT: Logout Button -->
      <div class="header-right">
        <button @click="handleLogout" class="nav-link logout-btn">로그아웃</button>
      </div>
    </div>
  </header>

  <main :style="showNavbar ? 'padding: 10px' : ''">
    <RouterView />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}


.header-left {
  display: flex;
  align-items: center;
  gap: 30px;
}

.main-nav {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-weight: 500;
  font-size: 1.1rem;
  transition: color 0.3s;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.nav-link:hover, .nav-link.router-link-active {
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.logout-btn {
  /* Ensure it looks like a link or styled button as needed */
  font-size: 1rem; 
  padding: 8px 16px;
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 20px;
}

.logout-btn:hover {
  background: rgba(255,255,255,0.1);
}

@media (min-width: 1024px) {
  header {
    /* override any vue cli defaults if necessary */
    /* display: flex; REMOVED - header is container */
    padding-right: 0;
  }
}
</style>
