// src/router.ts
import { createRouter, createWebHistory } from 'vue-router'
import Diagnosis from '../components/Diagnosis.vue'
import Login from '../components/Login.vue'
import Dashboard from '../components/Dashboard.vue'
import Home from '../components/Home.vue'
import Statistic from '../components/Statistic.vue'
import NewDiagnosis from '../components/NewDiagnosis.vue'

const routes = [
  {
    path: '/',
    component: Dashboard,
    children: [
      { path: '', name: 'Home', component: Home },
      {
        path: 'diagnosis',
        name: 'Diagnosis',
        component: Diagnosis,
        meta: { requiresAuth: true },
        children: [{ path: 'new', name: 'NewDiagnosis', component: NewDiagnosis, meta: { requiresAuth: true } }]
      },
      { path: 'statistic', name: 'Statistic', component: Statistic, meta: { requiresAuth: true } },
    ],
  },
  { path: '/auth', name: 'Login', component: Login },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard for authentication
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login' })
  } else if (to.name === 'Login' && token) {
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
