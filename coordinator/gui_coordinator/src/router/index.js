import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
    {
    path: '/budget',
    name: 'Budget',
    component: () => import('../views/BudgetView.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.NODE_ENV),
  routes
})

export default router
