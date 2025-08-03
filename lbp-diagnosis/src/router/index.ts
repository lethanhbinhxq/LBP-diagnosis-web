// src/router.ts
import { createRouter, createWebHistory } from 'vue-router'
// import Input from '../components/Input.vue'
import Diagnosis from '../components/Diagnosis.vue'
import Login from '../components/Login.vue'
import Dashboard from '../components/Dashboard.vue'
import Home from '../components/Home.vue'
import Statistic from '../components/Statistic.vue'
import Feedback from '../components/Feedback.vue'

const routes = [
  { path: '/', name: 'Login', component: Login },
  {
    path: '/dashboard',
    component: Dashboard,
    children: [
      { path: '', name: 'Home', component: Home },

      { path: 'diagnosis', name: 'Diagnosis', component: Diagnosis },
      { path: 'statistic', name: 'Statistic', component: Statistic },
      { path: 'feedback', name: 'Feedback', component: Feedback },
    ]
  },
]


const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
