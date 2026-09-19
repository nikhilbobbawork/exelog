import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/Dashboard.vue'
import ShipmentsView from '../views/Shipments.vue'
import AddShipmentView from '../views/AddShipment.vue'
import AddDriverView from '../views/AddDriver.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/shipments',
      name: 'shipments',
      component: ShipmentsView
    },
    {
      path: '/addshipment',
      name: 'addshipment',
      component: AddShipmentView
    },
    {
      path: '/addDriver',
      name: 'addDriver',
      component: AddDriverView
    },
  ]
})

export default router