export type VehicleType = 'passenger' | 'emergency' | 'bus' | 'truck';

export interface Position {
  lat: number;
  lng: number;
}

export interface Vehicle {
  id: string;
  type: VehicleType;
  position: Position;
  speed: number;
  lane: string;
  route: string[];
  color?: string;
  angle?: number;
}

export interface VehicleUpdate {
  id: string;
  position: Position;
  speed: number;
  angle?: number;
  timestamp: number;
}
