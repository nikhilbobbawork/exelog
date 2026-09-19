<template>
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md my-8">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Add New Shipment</h2>

    <!-- Error Message Display -->
    <div v-if="errorMessage" class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
      {{ errorMessage }}
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- Left Column: Shipment Form Fields -->
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Tracking Number (Optional)</label>
            <input 
              v-model="form.tracking_number" 
              type="text" 
              placeholder="Auto-generated if blank"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2 focus:border-indigo-500 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Driver Name</label>
            <select 
              v-model="form.driver_name" 
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2 focus:border-indigo-500 focus:ring-indigo-500 bg-white"
            >
              <option value="" disabled>Select a driver</option>
              <option v-for="driver in driverStore.drivers" :key="driver.id" :value="driver.name">
                {{ driver.name }} ({{ driver.status }})
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Status</label>
            <select 
              v-model="form.status"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2 focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="PENDING">PENDING</option>
              <option value="IN_TRANSIT">IN_TRANSIT</option>
              <option value="DELIVERED">DELIVERED</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Destination Address</label>
            <textarea 
              v-model="form.destination_address" 
              rows="2" 
              readonly
              class="mt-1 block w-full rounded-md bg-gray-50 border-gray-300 shadow-sm border p-2 text-gray-600"
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">City</label>
              <input v-model="form.destination_city" type="text" readonly class="mt-1 block w-full rounded-md bg-gray-50 border-gray-300 border p-2 text-gray-600" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Postal Code</label>
              <input v-model="form.destination_postal_code" type="text" readonly class="mt-1 block w-full rounded-md bg-gray-50 border-gray-300 border p-2 text-gray-600" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Country</label>
            <input v-model="form.destination_country" type="text" readonly class="mt-1 block w-full rounded-md bg-gray-50 border-gray-300 border p-2 text-gray-600" />
          </div>
        </div>

        <!-- Right Column: Map & Address Search -->
        <div class="space-y-4 flex flex-col">
          <label class="block text-sm font-medium text-gray-700">Select Destination on Map</label>
          
          <!-- Search Bar -->
          <div class="flex gap-2">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search address or location..."
              @keyup.enter.prevent="searchAddress"
              class="flex-1 rounded-md border-gray-300 shadow-sm border p-2 focus:border-indigo-500 focus:ring-indigo-500"
            />
            <button 
              type="button" 
              @click="searchAddress"
              :disabled="isSearching"
              class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {{ isSearching ? 'Searching...' : 'Search' }}
            </button>
          </div>

          <!-- Leaflet Map Container -->
          <div ref="mapContainer" class="w-full h-80 rounded-md border border-gray-300 z-0"></div>
          <p class="text-xs text-gray-500">Tip: Click anywhere on the map or drag the marker to automatically update the destination address fields.</p>
        </div>

      </div>

      <!-- Action Buttons -->
      <div class="flex justify-end gap-4 pt-4 border-t border-gray-200">
        <button 
          type="button" 
          @click="cancel"
          class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
        >
          Cancel
        </button>
        <button 
          type="submit" 
          :disabled="isSubmitting"
          class="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
        >
          {{ isSubmitting ? 'Creating...' : 'Create Shipment' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useShipmentStore } from '../stores/shipmentStore';
import { useDriverStore } from '../stores/driverStore';
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
const driverStore = useDriverStore();

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
  // Fetch drivers list for the select dropdown
  driverStore.fetchDrivers();

  if (!mapContainer.value) return;

  // Default coordinates (Chicago Hub)
  const defaultCoords = [41.8781, -87.6298];

  map = L.map(mapContainer.value).setView(defaultCoords, 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  marker = L.marker(defaultCoords, { draggable: true }).addTo(map);

  // Recalculate size to avoid tile-rendering glitches on initial load
  setTimeout(() => map?.invalidateSize(), 200);

  // Drag event listener
  marker.on('dragend', () => {
    const { lat, lng } = marker.getLatLng();
    reverseGeocode(lat, lng);
  });

  // Map click listener
  map.on('click', (e) => {
    const { lat, lng } = e.latlng;
    marker.setLatLng([lat, lng]);
    reverseGeocode(lat, lng);
  });
});

// Cleanup map instance on unmount
onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
  }
});

// Search address using OpenStreetMap Nominatim API
const searchAddress = async () => {
  if (!searchQuery.value.trim()) return;
  isSearching.value = true;
  errorMessage.value = '';

  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery.value)}`,
      {
        headers: {
          'User-Agent': 'ExelogApp/1.0'
        }
      }
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
    errorMessage.value = 'Failed to fetch location data.';
  } finally {
    isSearching.value = false;
  }
};

// Convert Lat/Lng into structured address components
const reverseGeocode = async (lat, lng) => {
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`,
      {
        headers: {
          'User-Agent': 'ExelogApp/1.0'
        }
      }
    );
    const data = await response.json();

    if (data) {
      const address = data.address || {};
      form.destination_address = data.display_name || '';
      form.destination_city = address.city || address.town || address.village || address.municipality || '';
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
    const payload = { ...form };
    if (!payload.tracking_number.trim()) {
      delete payload.tracking_number;
    }
    
    await shipmentStore.createShipment(payload);
    router.push('/shipments');
  } catch (error) {
    console.error('Submission error:', error);
    if (error.response?.data) {
      errorMessage.value = typeof error.response.data === 'string'
        ? error.response.data
        : JSON.stringify(error.response.data);
    } else {
      errorMessage.value = 'Failed to create shipment. Please check your input.';
    }
  } finally {
    isSubmitting.value = false;
  }
};

const cancel = () => {
  router.back();
};
</script>