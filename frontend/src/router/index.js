import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Auth/Login.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/Auth/Signup.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard/Dashboard.vue'),
      meta: { requiresAuth: true, role: 'STUDENT' }
    },
    {
      path: '/classroom/:id?',
      name: 'classroom',
      component: () => import('../views/Classroom/Classroom.vue'),
      meta: { requiresAuth: true, role: 'STUDENT' }
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: () => import('../views/MyPage/MyPage.vue'),
      meta: { requiresAuth: true, role: 'STUDENT' }
    },
    {
      path: '/instructor',
      name: 'instructor',
      component: () => import('../views/Instructor/InstructorDashboard.vue'),
      meta: { requiresAuth: true, role: 'INSTRUCTOR' }
    },
    {
      path: '/portfolio',
      name: 'portfolio',
      component: () => import('../views/Portfolio/PortfolioView.vue'),
      meta: { requiresAuth: true, role: 'STUDENT' }
    },
    {
      path: '/interview',
      name: 'interview',
      component: () => import('../views/Interview/InterviewView.vue'),
      meta: { requiresAuth: true, role: 'STUDENT' }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('auth_token')
  const userRole = localStorage.getItem('user_role')

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.role && to.meta.role !== userRole) {
    // Role mismatch redirect (e.g. Student trying to access Instructor page)
    next('/')
  } else {
    next()
  }
})

export default router
