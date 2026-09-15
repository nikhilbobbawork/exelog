<script setup>
import { ref, computed, onMounted } from 'vue'
import { useShipmentStore } from '../stores/shipmentStore'

const shipmentStore = useShipmentStore()

const searchQuery = ref('')
const selectedStatus = ref('ALL')

// Status Badge Tailwind Style Mapping
const statusBadgeStyles = {
  PENDING: 'bg-amber-100 text-amber-800 border border-amber-200',
  IN_TRANSIT: 'bg-blue-100 text-blue-800 border border-blue-200',
  DELIVERED: 'bg-emerald-100 text-emerald-800 border border-emerald-200',
}

// Fetch real data when component mounts
onMounted(() => {
  shipmentStore.fetchShipments()
})

// Filtered Shipments computed property
const filteredShipments = computed(() => {
  return shipmentStore.shipments.filter(item => {
    const tracking = item.tracking_number || ''
    const destination = item.destination || ''
    const driver = item.driver_name || ''
    const query = searchQuery.value.toLowerCase()

    const matchesSearch =
      tracking.toLowerCase().includes(query) ||
      destination.toLowerCase().includes(query) ||
      driver.toLowerCase().includes(query)

    const matchesStatus =
      selectedStatus.value === 'ALL' || item.status === selectedStatus.value

    return matchesSearch && matchesStatus
  })
})

// Quick status change handler
const updateStatus = async (shipment, newStatus) => {
  try {
    await shipmentStore.updateShipment(shipment.id, { status: newStatus })
  } catch (err) {
    console.error('Failed to update status:', err)
  }
}
</script>

<template>
  <div class="p-6 max-w-6xl mx-auto space-y-6">
    <!-- Header Summary -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-gray-200 pb-5">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">Shipment Dashboard</h1>
        <p class="text-sm text-gray-500 mt-1">Manage and track active logistics deliveries.</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="inline-flex items-center px-3 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
          Total: {{ shipmentStore.totalShipments }}
        </span>
      </div>
    </div>

    <!-- Search & Filter Controls -->
    <div class="flex flex-col sm:flex-row gap-4 justify-between items-center">
      <input 
        v-model="searchQuery" 
        type="text"
        placeholder="Search tracking #, address, or driver..." 
        class="w-full sm:w-80 px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm text-gray-900 placeholder-gray-400"
      />
      
      <select 
        v-model="selectedStatus" 
        class="w-full sm:w-48 px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm text-gray-700 bg-white"
      >
        <option value="ALL">All Statuses</option>
        <option value="PENDING">Pending ({{ shipmentStore.pendingCount }})</option>
        <option value="IN_TRANSIT">In Transit ({{ shipmentStore.inTransitCount }})</option>
        <option value="DELIVERED">Delivered ({{ shipmentStore.deliveredCount }})</option>
      </select>
    </div>

    <!-- Loading State -->
    <div v-if="shipmentStore.loading" class="flex justify-center items-center py-12 text-gray-500 font-medium">
      <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Loading shipments...
    </div>
    
    <!-- Error State -->
    <div v-else-if="shipmentStore.error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm font-medium">
      {{ shipmentStore.error }}
    </div>

    <!-- Data Table -->
    <div v-else class="overflow-x-auto bg-white rounded-lg border border-gray-200 shadow-sm">
      <table class="w-full text-left border-collapse">
        <thead class="bg-gray-50 border-b border-gray-200 text-xs uppercase font-semibold text-gray-500 tracking-wider">
          <tr>
            <th class="px-6 py-3">Tracking #</th>
            <th class="px-6 py-3">Destination</th>
            <th class="px-6 py-3">Driver</th>
            <th class="px-6 py-3">Status</th>
            <th class="px-6 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 text-sm">
          <tr 
            v-for="shipment in filteredShipments" 
            :key="shipment.id"
            class="hover:bg-gray-50 transition-colors"
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
            <td class="px-6 py-4 text-right">
              <select
                :value="shipment.status"
                @change="e => updateStatus(shipment, e.target.value)"
                class="text-xs border border-gray-300 rounded px-2 py-1 bg-white text-gray-700 focus:outline-none focus:ring-1 focus:ring-indigo-500 cursor-pointer"
              >
                <option value="PENDING">Pending</option>
                <option value="IN_TRANSIT">In Transit</option>
                <option value="DELIVERED">Delivered</option>
              </select>
            </td>
          </tr>
          
          <tr v-if="filteredShipments.length === 0">
            <td colspan="5" class="px-6 py-12 text-center text-gray-500">
              No shipments found matching your criteria.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>