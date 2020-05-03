import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Dependents from "../views/Dependents";
import Parsing from "../views/Parsing";

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
  },
  {
    path: '/dependents/parsing/:group/:project',
    name: 'Parsing',
    component: Parsing,
  }
]

const router = new VueRouter({
  routes
})

export default router
