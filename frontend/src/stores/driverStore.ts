// stores/driverStore.ts
import { defineStore } from 'pinia';
import axios from 'axios';

export interface Driver {
  id: number;
  name: string;
  phone: string;
  license_number?: string;
  status: 'AVAILABLE' | 'ON_ROUTE' | 'OFF_DUTY';
  assigned_shipments_count?: number;
}

export const useDriverStore = defineStore('driver', {
  state: () => ({
    drivers: [] as Driver[],
    loading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchDrivers(statusFilter?: string) {
      this.loading = true;
      try {
        const url = statusFilter ? `/api/drivers/?status=${statusFilter}` : '/api/drivers/';
        const response = await axios.get(url);
        this.drivers = response.data;
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch drivers';
      } finally {
        this.loading = false;
      }
    },
    async createDriver(payload: Partial<Driver>) {
      const response = await axios.post('/api/drivers/', payload);
      this.drivers.unshift(response.data);
      return response.data;
    }
  }
});