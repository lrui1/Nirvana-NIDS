import { createRouter, createWebHistory } from 'vue-router'
import Layout from './components/Layout.vue'
import Overview from './views/Overview.vue'
import Details from './views/Details.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '',
        redirect: '/overview'
      },
      {
        path: '/overview',
        component: Overview
      },
      {
        path: '/details',
        component: Details
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 