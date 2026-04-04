import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import ItemsView from '../views/ItemsView.vue'

const routes = [
  { path: '/', component: LoginView },
  {
    path: '/items',
    component: ItemsView,
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