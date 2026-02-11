<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper glass-container" style="margin: 20px; display: flex; justify-content: space-between; align-items: center;">
      <div class="logo">
        <h2 style="margin: 0; color: #fff;">Re:Boot</h2>
      </div>

      <nav>
        <RouterLink to="/" class="nav-link">Dashboard</RouterLink>
        <RouterLink to="/classroom" class="nav-link">Classroom</RouterLink>
        <RouterLink to="/mypage" class="nav-link">MyPage</RouterLink>
        <RouterLink to="/instructor" class="nav-link">Instructor</RouterLink>
      </nav>
    </div>
  </header>

  <main style="padding: 20px;">
    <RouterView />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-weight: 500;
  margin-left: 20px;
  font-size: 1.1rem;
  transition: color 0.3s;
}

.nav-link:hover, .nav-link.router-link-active {
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }
}
</style>
