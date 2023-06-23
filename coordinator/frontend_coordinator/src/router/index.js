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
    path: '/clubs',
    name: 'Clubs',
    component: () => import('../views/ClubsView.vue')
  },
  {
    path: '/rinkmanager',
    name: 'Manage Rinks',
    component: () => import('../views/RinkManager.vue')
  },
  {
    path: '/support',
    name: 'Support',
    component: () => import('../views/Support.vue')
  },
]

const router = createRouter({
  mode: 'history',
  history: createWebHistory('/#'),
  routes
})

export default router
