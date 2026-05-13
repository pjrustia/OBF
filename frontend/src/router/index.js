import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import ItemsView from '../views/ItemsView.vue'
import ReportView from '../views/ReportView.vue'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  { path: '/', component: LoginView },
  {
    path: '/dashboard',
    component: DashboardView,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem('token')) next('/')
      else next()
    }
  },
  {
    path: '/items',
    component: ItemsView,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem('token')) next('/')
      else next()
    }
  },
  {
    path: '/report',
    component: ReportView,
    beforeEnter: (to, from, next) => {
      if (!localStorage.getItem('token')) next('/')
      else next()
    }
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})