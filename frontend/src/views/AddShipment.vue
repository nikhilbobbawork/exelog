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
            Tracking Number <span class="text-xs text-gray-400 font-normal">(Leave blank to auto-generate)</span>
          </label>
          <input 
            id="trackingNumber"
            v-model="form.tracking_number" 
            type="text" 
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

        <!-- MAP ADDRESS PICKER SECTION -->
        <div class="sm:col-span-2 space-y-3">
          <label class="block text-sm font-medium text-gray-700">
            Destination Address & Location Pin <span class="text-red-500">*</span>
          </label>
          
          <!-- Search Bar -->
          <div class="flex gap-2">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search location on map..." 
              @keyup.enter.prevent="searchAddress"
              class="w-full px-3.5 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm text-gray-900"
            />
            <button 
              type="button" 
              @click="searchAddress" 
              :disabled="isSearching"
              class="px-4 py-2 bg-gray-800 hover:bg-gray-900 text-white text-sm font-medium rounded-lg shadow-sm transition-colors"
            >
              {{ isSearching ? 'Searching...' : 'Search' }}
            </button>
          </div>

          <!-- Leaflet Map Container -->
          <div ref="mapContainer" class="h-64 w-full rounded-lg border border-gray-300 shadow-inner z-0"></div>
          <p class="text-xs text-gray-500">Tip: Click anywhere on the map or drag the blue marker to pinpoint exact drop-off coordinates.</p>

          <!-- Formatted Address Result -->
          <div>
            <label for="destinationAddress" class="block text-xs font-semibold text-gray-600 mb-1">Formatted Address</label>
            <input 
              id="destinationAddress"
              v-model="form.destination_address" 
              type="text" 
              required
              placeholder="Address will auto-fill from map marker"
              class="w-full px-3.5 py-2 border border-gray-300 rounded-lg shadow-sm bg-gray-50 text-sm text-gray-900"
            />
          </div>

          <!-- Extra Address Breakdown & Coordinates -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
            <div>
              <label class="block text-xs font-medium text-gray-500">City</label>
              <input v-model="form.destination_city" type="text" class="w-full p-2 border border-gray-200 rounded text-xs bg-gray-50" readonly />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500">Postal Code</label>
              <input v-model="form.destination_postal_code" type="text" class="w-full p-2 border border-gray-200 rounded text-xs bg-gray-50" readonly />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500">Latitude</label>
              <input :value="form.destination_lat ?? ''" type="text" class="w-full p-2 border border-gray-200 rounded text-xs bg-gray-50" readonly />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500">Longitude</label>
              <input :value="form.destination_lng ?? ''" type="text" class="w-full p-2 border border-gray-200 rounded text-xs bg-gray-50" readonly />
            </div>
          </div>
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
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useShipmentStore } from '../stores/shipmentStore';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix default Leaflet icon paths in Vue/Vite builds
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl,
  iconRetinaUrl,
  shadowUrl,
});

const router = useRouter();
const shipmentStore = useShipmentStore();
const isSubmitting = ref(false);
const isSearching = ref(false);
const errorMessage = ref('');

const mapContainer = ref(null);
const searchQuery = ref('');
let map = null;
let marker = null;

const form = reactive({
  tracking_number: '',
  destination_address: '',
  destination_city: '',
  destination_postal_code: '',
  destination_country: '',
  destination_lat: null,
  destination_lng: null,
  driver_name: '',
  status: 'PENDING',
});

onMounted(() => {
  // Default coordinates (e.g., Chicago / Central Hub)
  const defaultCoords = [41.8781, -87.6298];

  map = L.map(mapContainer.value).setView(defaultCoords, 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  marker = L.marker(defaultCoords, { draggable: true }).addTo(map);

  // Handle marker drag event
  marker.on('dragend', () => {
    const { lat, lng } = marker.getLatLng();
    reverseGeocode(lat, lng);
  });

  // Handle direct map click event
  map.on('click', (e) => {
    const { lat, lng } = e.latlng;
    marker.setLatLng([lat, lng]);
    reverseGeocode(lat, lng);
  });
});

// Search address using OpenStreetMap Nominatim API
const searchAddress = async () => {
  if (!searchQuery.value.trim()) return;
  isSearching.value = true;
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery.value)}`
    );
    const data = await response.json();
    if (data && data.length > 0) {
      const result = data[0];
      const lat = parseFloat(result.lat);
      const lng = parseFloat(result.lon);
      
      marker.setLatLng([lat, lng]);
      map.panTo([lat, lng]);
      
      reverseGeocode(lat, lng);
    } else {
      errorMessage.value = 'Address not found. Please try a different search query.';
    }
  } catch (err) {
    console.error('Search error:', err);
  } finally {
    isSearching.value = false;
  }
};

// Convert Lat/Lng into structured address components
const reverseGeocode = async (lat, lng) => {
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
    );
    const data = await response.json();
    if (data) {
      const address = data.address || {};
      form.destination_address = data.display_name || '';
      form.destination_city = address.city || address.town || address.village || '';
      form.destination_postal_code = address.postcode || '';
      form.destination_country = address.country || '';
      form.destination_lat = parseFloat(lat.toFixed(6));
      form.destination_lng = parseFloat(lng.toFixed(6));
    }
  } catch (err) {
    console.error('Reverse geocoding error:', err);
  }
};

const handleSubmit = async () => {
  isSubmitting.value = true;
  errorMessage.value = '';
  try {
    // If tracking number is blank, delete key so backend auto-generates it
    const payload = { ...form };
    if (!payload.tracking_number) {
      delete payload.tracking_number;
    }
    
    await shipmentStore.createShipment(payload);
    router.push('/shipments');
  } catch (error) {
    console.error('Submission error:', error);
    errorMessage.value = error.response?.data ? JSON.stringify(error.response.data) : 'Failed to create shipment.';
  } finally {
    isSubmitting.value = false;
  }
};

const cancel = () => {
  router.back();
};
</script>