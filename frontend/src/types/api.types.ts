import { Scenario, SimulationMetrics, SimulationState } from './simulation.types';
import { Vehicle, VehicleUpdate } from './vehicle.types';
import { TrafficLight, TrafficLightUpdate } from './traffic.types';

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface StartSimulationRequest {
  scenarioId?: string;
  speedMultiplier?: number;
  optimizationMode?: boolean;
}

export interface EmergencyVehicleRequest {
  origin: string;
  destination: string;
  priority?: number;
}

export interface WebSocketMessage {
  type: 'simulation_update' | 'vehicle_update' | 'traffic_light_update' | 'metrics_update';
  data: unknown;
  timestamp: number;
}

export interface SimulationUpdateData {
  simulationTime: number;
  vehicles: Vehicle[];
  trafficLights: TrafficLight[];
  metrics: SimulationMetrics;
  state: SimulationState;
}

export interface VehicleUpdateData {
  updates: VehicleUpdate[];
}

export interface TrafficLightUpdateData {
  updates: TrafficLightUpdate[];
}

export interface MetricsUpdateData {
  metrics: SimulationMetrics;
}
