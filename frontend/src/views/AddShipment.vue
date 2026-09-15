<template>
  <div class="p-6 max-w-3xl mx-auto space-y-6">
    <!-- Form Header -->
    <div class="border-b border-gray-200 pb-5">
      <h2 class="text-2xl font-bold text-gray-900 tracking-tight">Create New Shipment</h2>
      <p class="text-sm text-gray-500 mt-1">Fill out the information below to register a new order into the system.</p>
    </div>

    <div v-if="errorMessage" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm font-medium">
      {{ errorMessage }}
    </div>
    <!-- Form Container -->
    <form @submit.prevent="handleSubmit" class="bg-white rounded-xl border border-gray-200 shadow-sm p-6 space-y-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        
        <!-- Tracking Number -->
        <div class="sm:col-span-1">
          <label for="trackingNumber" class="block text-sm font-medium text-gray-700 mb-1">
            Tracking Number <span class="text-red-500">*</span>
          </label>
          <input 
            id="trackingNumber"
            v-model="form.tracking_number" 
            type="text" 
            required
            placeholder="e.g. TRK-984210"
            class="w-full px-3.5 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm text-gray-900 placeholder-gray-400 font-mono"
          />
        </div>

        <!-- Status Selection -->
        <div class="sm:col-span-1">
          <label for="status" class="block text-sm font-medium text-gray-700 mb-1">
            Initial Status
          </label>
          <select 
            id="status"
            v-model="form.status" 
            class="w-full px-3.5 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm text-gray-900 bg-white"
          >
            <option value="PENDING">Pending</option>
            <option value="IN_TRANSIT">In Transit</option>
            <option value="DELIVERED">Delivered</option>
          </select>
        </div>

        <!-- Destination -->
        <div class="sm:col-span-2">
          <label for="destination" class="block text-sm font-medium text-gray-700 mb-1">
            Destination Address <span class="text-red-500">*</span>
          </label>
          <input 
            id="destination"
            v-model="form.destination" 
            type="text" 
            required
            placeholder="e.g. 742 Evergreen Terrace, Springfield, IL"
            class="w-full px-3.5 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm text-gray-900 placeholder-gray-400"
          />
        </div>

        <!-- Assigned Driver -->
        <div class="sm:col-span-2">
          <label for="driverName" class="block text-sm font-medium text-gray-700 mb-1">
            Assigned Driver <span class="text-xs text-gray-400 font-normal">(Optional)</span>
          </label>
          <input 
            id="driverName"
            v-model="form.driver_name" 
            type="text" 
            placeholder="e.g. Ajunta Pal"
            class="w-full px-3.5 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm text-gray-900 placeholder-gray-400"
          />
        </div>

      </div>

      <!-- Action Buttons -->
      <div class="flex items-center justify-end gap-3 pt-4 border-t border-gray-100">
        <button 
          type="button" 
          @click="cancel"
          class="px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-700 text-sm font-medium rounded-lg shadow-sm transition-colors cursor-pointer"
        >
          Cancel
        </button>
        <button 
          type="submit" 
          :disabled="isSubmitting"
          class="inline-flex items-center justify-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 cursor-pointer"
        >
          {{ isSubmitting ? 'Saving...' : 'Create Shipment' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useShipmentStore } from '../stores/shipmentStore';

const router = useRouter();
const shipmentStore = useShipmentStore();
const isSubmitting = ref(false);

const form = reactive({
  tracking_number: '',
  destination: '',
  driver_name: '',
  status: 'PENDING',
});

const handleSubmit = async () => {
  isSubmitting.value = true;
  try {
    await shipmentStore.createShipment({ ...form });
    router.push('/shipments');
  } catch (error) {
    console.error('Submission error:', error);
  } finally {
    isSubmitting.value = false;
  }
};

const cancel = () => {
  router.back();
};
</script>