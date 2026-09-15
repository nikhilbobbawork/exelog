import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/Dashboard.vue'
import ShipmentsView from '../views/Shipments.vue'
import AddShipmentView from '../views/AddShipment.vue'

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
    }
  ]
})

export default router