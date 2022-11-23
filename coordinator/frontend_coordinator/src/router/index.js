import { createRouter, createWebHistory } from 'vue-router'
import Coordinator from '../views/Coordinator.vue'

const routes = [
  {
    path: '/',
    name: 'Coordinator',
    component: Coordinator
  },
    {
    path: '/players',
    name: 'Players',
    component: () => import('../views/PlayersView.vue')
  },
  {
    path: '/teams',
    name: 'Teams',
    component: () => import('../views/TeamsView.vue')
  },
  {
    path: '/rinkmanager',
    name: 'Manage Rinks',
    component: () => import('../views/RinkManager.vue')
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
