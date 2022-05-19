import { createRouter, createWebHistory } from 'vue-router'
import Backboard from '../components/Backboard.vue'
import Sponsor from '../components/Sponsor.vue'
import Weather from '../components/Weather.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: Backboard,
        },
        {
            path: '/sponsor',
            component: Sponsor,
        },
        {
            path: '/weather',
            component: Weather,
        },
    ],
})

export default router

