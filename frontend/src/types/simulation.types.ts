export interface SimulationMetrics {
  timestamp: string;
  totalVehicles: number;
  avgSpeed: number;
  avgTravelTime: number;
  co2Emissions: number;
  queueLengths: Record<string, number>;
  emergencyVehiclesActive: number;
  completedTrips: number;
  waitingTime: number;
}

export interface SimulationState {
  isRunning: boolean;
  isPaused: boolean;
  currentScenario: string | null;
  simulationTime: number;
  speedMultiplier: number;
  optimizationMode: boolean;
}

export interface Scenario {
  id: string;
  name: string;
  description: string;
  vehicleCount: number;
  duration: number;
  emergencyVehicles: number;
  rushHourMode: boolean;
  createdAt: string;
  config?: Record<string, unknown>;
}

export interface SimulationConfig {
  stepLength: number;
  begin: number;
  end: number;
  seed?: number;
  gui?: boolean;
}

export interface PerformanceMetrics {
  scenarioName: string;
  avgSpeed: number;
  avgTravelTime: number;
  totalEmissions: number;
  avgQueueLength: number;
  timestamp: string;
}
