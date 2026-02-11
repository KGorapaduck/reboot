import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard/Dashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/classroom/:id?',
      name: 'classroom',
      component: () => import('../views/Classroom/Classroom.vue')
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: () => import('../views/MyPage/MyPage.vue')
    },
    {
      path: '/instructor',
      name: 'instructor',
      component: () => import('../views/Instructor/InstructorDashboard.vue')
    }
  ]
})

export default router
