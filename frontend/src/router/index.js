import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import ItemsView from '../views/ItemsView.vue'
import ReportView from '../views/ReportView.vue'
import DashboardView from '../views/DashboardView.vue'
import ItemDetailView from '../views/ItemDetailView.vue'

const isLoggedIn = () => !!localStorage.getItem('token')

const routes = [
  { path: '/', component: LoginView },
  {
    path: '/dashboard',
    component: DashboardView,
    beforeEnter: () => isLoggedIn() || '/'
  },
  {
    path: '/items',
    component: ItemsView,
    beforeEnter: () => isLoggedIn() || '/'
  },
  {
    path: '/items/:id',
    component: ItemDetailView,
    beforeEnter: () => isLoggedIn() || '/'
  },
  {
    path: '/report',
    component: ReportView,
    beforeEnter: () => isLoggedIn() || '/'
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})