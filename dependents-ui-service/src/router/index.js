import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Dependents from "../views/Dependents";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/dependents/analysis/:group/:project',
    name: 'Analysis',
    component: Dependents,

  }
]

const router = new VueRouter({
  routes
})

export default router
