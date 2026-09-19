<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useShipmentStore } from '../stores/shipmentStore'

const router = useRouter()
const shipmentStore = useShipmentStore()

// Status Badge Tailwind Style Mapping
const statusBadgeStyles = {
  PENDING: 'bg-amber-100 text-amber-800 border border-amber-200',
  IN_TRANSIT: 'bg-blue-100 text-blue-800 border border-blue-200',
  DELIVERED: 'bg-emerald-100 text-emerald-800 border border-emerald-200',
}

onMounted(() => {
  if (shipmentStore.shipments.length === 0) {
    shipmentStore.fetchShipments()
  }
})

// Metrics directly using Pinia store getters/state
const totalShipments = computed(() => shipmentStore.totalShipments || shipmentStore.shipments.length)
const pendingCount = computed(() => shipmentStore.pendingCount)
const inTransitCount = computed(() => shipmentStore.inTransitCount)
const deliveredCount = computed(() => shipmentStore.deliveredCount)

// Recent activity feed (latest 5 created)
const recentShipments = computed(() => {
  return [...shipmentStore.shipments]
    .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
    .slice(0, 5)
})

const navigateToShipments = () => {
  router.push('/shipments')
}
</script>

<template>
  <div class="p-6 max-w-7xl mx-auto space-y-8">
    <!-- Header Summary Section -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-6 border-b border-gray-200">
      <div>
        <h2 class="text-2xl font-bold text-gray-900 tracking-tight">System Overview</h2>
        <p class="text-sm text-gray-500 mt-1">Real-time status of current logistics operations.</p>
      </div>
      <button 
        @click="navigateToShipments" 
        class="inline-flex items-center justify-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 cursor-pointer"
      >
        View All Shipments &rarr;
      </button>
    </div>

    <!-- KPI Metric Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <!-- Total Active -->
      <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between space-y-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-gray-500">Total Managed</span>
        <div class="text-3xl font-extrabold text-gray-900">{{ totalShipments }}</div>
        <span class="text-xs text-gray-500">All system records</span>
      </div>

      <!-- Pending Dispatch -->
      <div class="bg-white p-5 rounded-xl border border-gray-200 border-l-4 border-l-amber-500 shadow-sm flex flex-col justify-between space-y-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-amber-700">Pending Dispatch</span>
        <div class="text-3xl font-extrabold text-gray-900">{{ pendingCount }}</div>
        <span class="text-xs text-gray-500">Awaiting assignment</span>
      </div>

      <!-- In Transit -->
      <div class="bg-white p-5 rounded-xl border border-gray-200 border-l-4 border-l-blue-500 shadow-sm flex flex-col justify-between space-y-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-blue-700">In Transit</span>
        <div class="text-3xl font-extrabold text-gray-900">{{ inTransitCount }}</div>
        <span class="text-xs text-gray-500">En route to destination</span>
      </div>

      <!-- Delivered -->
      <div class="bg-white p-5 rounded-xl border border-gray-200 border-l-4 border-l-emerald-500 shadow-sm flex flex-col justify-between space-y-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-emerald-700">Delivered</span>
        <div class="text-3xl font-extrabold text-gray-900">{{ deliveredCount }}</div>
        <span class="text-xs text-gray-500">Completed deliveries</span>
      </div>
    </div>

    <!-- Recent Activity Section -->
    <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      <div class="p-5 border-b border-gray-200 flex items-center justify-between">
        <h3 class="text-base font-semibold text-gray-900">Recent Shipment Activity</h3>
        <button 
          @click="navigateToShipments" 
          class="text-xs font-medium text-indigo-600 hover:text-indigo-800 cursor-pointer transition-colors"
        >
          View Full Table &rarr;
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="shipmentStore.loading" class="p-8 text-center text-sm font-medium text-gray-500">
        Loading metrics...
      </div>

      <!-- Error State -->
      <div v-else-if="shipmentStore.error" class="p-4 m-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm font-medium">
        {{ shipmentStore.error }}
      </div>

      <!-- Recent Shipments Table -->
      <div v-else-if="recentShipments.length > 0" class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead class="bg-gray-50 border-b border-gray-200 text-xs uppercase font-semibold text-gray-500 tracking-wider">
            <tr>
              <th class="px-6 py-3">Tracking #</th>
              <th class="px-6 py-3">Destination</th>
              <th class="px-6 py-3">Driver</th>
              <th class="px-6 py-3">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 text-sm">
            <tr 
              v-for="shipment in recentShipments" 
              :key="shipment.id"
              class="hover:bg-gray-50 transition-colors cursor-pointer"
              @click="navigateToShipments"
            >
              <td class="px-6 py-4 font-semibold text-gray-900 font-mono">
                {{ shipment.tracking_number }}
              </td>
              <td class="px-6 py-4 text-gray-700 max-w-xs truncate">
                {{ shipment.destination }}
              </td>
              <td class="px-6 py-4 text-gray-600">
                <span :class="{'italic text-gray-400': !shipment.driver_name}">
                  {{ shipment.driver_name || 'Unassigned' }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span 
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide',
                    statusBadgeStyles[shipment.status] || 'bg-gray-100 text-gray-800'
                  ]"
                >
                  {{ (shipment.status || '').replace('_', ' ') }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-else class="p-8 text-center text-sm text-gray-500">
        No shipments registered in the system yet.
      </div>
    </div>
  </div>
</template>