<template>
  <div class="max-w-6xl mx-auto p-6 bg-white rounded-lg shadow-md my-8">
    <!-- Header & Action Button -->
    <div class="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">Driver Management</h2>
        <p class="text-sm text-gray-500">Monitor and manage active drivers and their statuses.</p>
      </div>
      <button 
        @click="showAddModal = true"
        class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition"
      >
        + Add New Driver
      </button>
    </div>

    <!-- Error / Loading States -->
    <div v-if="driverStore.error" class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
      {{ driverStore.error }}
    </div>

    <!-- Filters -->
    <div class="flex items-center gap-4 mb-6">
      <label class="text-sm font-medium text-gray-700">Filter Status:</label>
      <select 
        v-model="selectedStatus" 
        @change="fetchFilteredDrivers"
        class="rounded-md border-gray-300 shadow-sm border p-2 text-sm focus:border-indigo-500 focus:ring-indigo-500"
      >
        <option value="">All Statuses</option>
        <option value="AVAILABLE">AVAILABLE</option>
        <option value="ON_ROUTE">ON ROUTE</option>
        <option value="OFF_DUTY">OFF DUTY</option>
      </select>
    </div>

    <!-- Drivers Table -->
    <div class="overflow-x-auto border border-gray-200 rounded-lg">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phone</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">License Number</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="driverStore.loading">
            <td colspan="4" class="px-6 py-4 text-center text-gray-500">Loading drivers...</td>
          </tr>
          <tr v-else-if="driverStore.drivers.length === 0">
            <td colspan="4" class="px-6 py-4 text-center text-gray-500">No drivers found.</td>
          </tr>
          <tr v-for="driver in driverStore.drivers" :key="driver.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{{ driver.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-600">{{ driver.phone }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-gray-600">{{ driver.license_number || 'N/A' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="{
                'px-2 inline-flex text-xs leading-5 font-semibold rounded-full': true,
                'bg-green-100 text-green-800': driver.status === 'AVAILABLE',
                'bg-blue-100 text-blue-800': driver.status === 'ON_ROUTE',
                'bg-gray-100 text-gray-800': driver.status === 'OFF_DUTY'
              }">
                {{ driver.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add Driver Modal / Form Drawer -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg max-w-md w-full p-6 shadow-xl">
        <h3 class="text-xl font-bold mb-4 text-gray-800">Add New Driver</h3>
        
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Driver Name</label>
            <input 
              v-model="newDriver.name" 
              type="text" 
              required
              placeholder="e.g. John Doe"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2 focus:border-indigo-500 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Phone Number</label>
            <input 
              v-model="newDriver.phone" 
              type="text" 
              required
              placeholder="e.g. +1 555-0192"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2 focus:border-indigo-500 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">License Number (Optional)</label>
            <input 
              v-model="newDriver.license_number" 
              type="text" 
              placeholder="e.g. DL-982341"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2 focus:border-indigo-500 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Status</label>
            <select 
              v-model="newDriver.status"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2 focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="AVAILABLE">AVAILABLE</option>
              <option value="ON_ROUTE">ON ROUTE</option>
              <option value="OFF_DUTY">OFF DUTY</option>
            </select>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button 
              type="button" 
              @click="showAddModal = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              :disabled="isSubmitting"
              class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {{ isSubmitting ? 'Saving...' : 'Save Driver' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useDriverStore } from '../stores/driverStore';

const driverStore = useDriverStore();
const selectedStatus = ref('');
const showAddModal = ref(false);
const isSubmitting = ref(false);

const newDriver = reactive({
  name: '',
  phone: '',
  license_number: '',
  status: 'AVAILABLE',
});

onMounted(() => {
  driverStore.fetchDrivers();
});

const fetchFilteredDrivers = () => {
  driverStore.fetchDrivers(selectedStatus.value);
};

const handleSubmit = async () => {
  isSubmitting.value = true;
  try {
    await driverStore.createDriver(newDriver);
    // Reset form and close modal
    newDriver.name = '';
    newDriver.phone = '';
    newDriver.license_number = '';
    newDriver.status = 'AVAILABLE';
    showAddModal.value = false;
  } catch (err) {
    console.error('Failed to create driver:', err);
  } finally {
    isSubmitting.value = false;
  }
};
</script>