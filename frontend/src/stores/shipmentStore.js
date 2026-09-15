// src/stores/shipmentStore.js
import { defineStore } from 'pinia'
import api from '../api/axios.js'

export const useShipmentStore = defineStore('shipment', {
  state: () => ({
    shipments: [],
    currentShipment: null,
    loading: false,
    error: null,
    // Active query parameters matching Django Filter & Search backends
    filters: {
      search: '',
      status: '', // 'PENDING', 'IN_TRANSIT', 'DELIVERED', or '' (all)
    },
  }),

  getters: {
    /** Total shipment count */
    totalShipments: (state) => state.shipments.length,

    /** Filtered breakdown counts for UI metrics/tabs */
    pendingCount: (state) =>
      state.shipments.filter((s) => s.status === 'PENDING').length,

    inTransitCount: (state) =>
      state.shipments.filter((s) => s.status === 'IN_TRANSIT').length,

    deliveredCount: (state) =>
      state.shipments.filter((s) => s.status === 'DELIVERED').length,
  },

  actions: {
    /**
     * Fetch all shipments with optional search and status filtering
     */
    async fetchShipments() {
      this.loading = true
      this.error = null

      try {
        const params = {}
        if (this.filters.search.trim()) {
          params.search = this.filters.search.trim()
        }
        if (this.filters.status) {
          params.status = this.filters.status
        }

        const response = await api.get('shipments/', { params })
        // Handles both DRF paginated responses ({ results: [...] }) and plain arrays
        this.shipments = Array.isArray(response.data)
          ? response.data
          : response.data.results || []
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to load shipments.'
      } finally {
        this.loading = false
      }
    },

    /**
     * Fetch a single shipment by primary key / UUID
     */
    async fetchShipmentById(id) {
      this.loading = true
      this.error = null

      try {
        const response = await api.get(`shipments/${id}/`)
        this.currentShipment = response.data
        return response.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Shipment not found.'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * Create a new shipment
     * @param {Object} payload - { destination, driver_name, status, tracking_number? }
     */
    async createShipment(payload) {
      this.loading = true
      this.error = null

      try {
        const response = await api.post('shipments/', payload)
        // Add newly created shipment to local state immediately
        this.shipments.unshift(response.data)
        return response.data
      } catch (err) {
        this.error = err.response?.data || 'Failed to create shipment.'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * Update an existing shipment (partial update using PATCH)
     * @param {number|string} id 
     * @param {Object} updates - Fields to update (e.g., { status: 'DELIVERED' })
     */
    async updateShipment(id, updates) {
      this.loading = true
      this.error = null

      try {
        const response = await api.patch(`shipments/${id}/`, updates)
        
        // Update item in local shipments list
        const index = this.shipments.findIndex((s) => s.id === id)
        if (index !== -1) {
          this.shipments[index] = response.data
        }

        if (this.currentShipment?.id === id) {
          this.currentShipment = response.data
        }

        return response.data
      } catch (err) {
        this.error = err.response?.data || 'Failed to update shipment.'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * Delete a shipment record
     * @param {number|string} id 
     */
    async deleteShipment(id) {
      this.loading = true
      this.error = null

      try {
        await api.delete(`shipments/${id}/`)
        this.shipments = this.shipments.filter((s) => s.id !== id)
        if (this.currentShipment?.id === id) {
          this.currentShipment = null
        }
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to delete shipment.'
        throw err
      } finally {
        this.loading = false
      }
    },

    /**
     * Update filter criteria and trigger re-fetch
     */
    setSearchQuery(query) {
      this.filters.search = query
      this.fetchShipments()
    },

    setStatusFilter(status) {
      this.filters.status = status
      this.fetchShipments()
    },
  },
})