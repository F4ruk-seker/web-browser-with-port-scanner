import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/views/HomeView.vue";

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/target/:target_id',
        name: 'target',
        component: () => import(/* webpackChunkName: "projects" */ '../views/TargetView.vue'),
        props: true
    },
]

const router = createRouter({
    history: createWebHistory("./"),
    routes
})

export default router
