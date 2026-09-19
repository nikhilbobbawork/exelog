export type DriverStatus = 'AVAILABLE' | 'ON_ROUTE' | 'OFF_DUTY';
export type ShipmentStatus = 'PENDING' | 'IN_TRANSIT' | 'DELIVERED';

export interface Driver {
  id: number;
  name: string;
  phone: string;
  license_number?: string;
  status: DriverStatus;
  status_display: string;
  created_at: string;
  updated_at: string;
}

export interface Shipment {
  id: number;
  tracking_number: string;
  destination_address: string;
  destination_city: string;
  destination_postal_code: string;
  destination_country: string;
  destination_lat: number | null;
  destination_lng: number | null;
  driver: number | null;
  driver_detail: Driver | null;
  status: ShipmentStatus;
  status_display: string;
  created_at: string;
  updated_at: string;
}

export interface ShipmentFilters {
  status?: ShipmentStatus | '';
  driver?: number | null;
  search?: string;
}