export const API_ENDPOINTS = {
  SCENARIOS: '/api/scenarios',
  SIMULATION_START: '/api/simulation/start',
  SIMULATION_STOP: '/api/simulation/stop',
  SIMULATION_STATUS: '/api/simulation/status',
  METRICS: '/api/metrics',
  EMERGENCY_VEHICLE: '/api/simulation/emergency',
} as const;

export const WS_EVENTS = {
  CONNECT: 'connect',
  DISCONNECT: 'disconnect',
  SIMULATION_UPDATE: 'simulation_update',
  VEHICLE_UPDATE: 'vehicle_update',
  TRAFFIC_LIGHT_UPDATE: 'traffic_light_update',
  METRICS_UPDATE: 'metrics_update',
} as const;

export const DEFAULT_MAP_CENTER = {
  lat: 48.8566,
  lng: 2.3522,
};

export const DEFAULT_MAP_ZOOM = 13;

export const SIMULATION_SPEED_OPTIONS = [0.5, 1, 2, 5, 10];

export const VEHICLE_COLORS = {
  passenger: '#3b82f6',
  emergency: '#ef4444',
  bus: '#10b981',
  truck: '#8b5cf6',
} as const;

export const TRAFFIC_LIGHT_COLORS = {
  G: '#22c55e',
  g: '#22c55e',
  y: '#eab308',
  Y: '#eab308',
  r: '#ef4444',
  R: '#ef4444',
} as const;
