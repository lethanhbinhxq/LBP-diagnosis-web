// src/router.ts
import { createRouter, createWebHistory } from 'vue-router'
import Input from '../components/Input.vue'
import Diagnosis from '../components/Diagnosis.vue'

const routes = [
  { path: '/', name: 'Input', component: Input },
  { path: '/diagnosis', name: 'Diagnosis', component: Diagnosis }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
