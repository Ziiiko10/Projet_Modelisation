import { create } from 'zustand';
import { Vehicle, TrafficLight, SimulationState, SimulationMetrics, Scenario } from '../types';

interface SimulationStore {
  state: SimulationState;
  vehicles: Map<string, Vehicle>;
  trafficLights: Map<string, TrafficLight>;
  metrics: SimulationMetrics | null;
  scenarios: Scenario[];
  currentScenario: Scenario | null;

  setState: (state: Partial<SimulationState>) => void;
  setVehicles: (vehicles: Vehicle[]) => void;
  updateVehicle: (id: string, updates: Partial<Vehicle>) => void;
  removeVehicle: (id: string) => void;
  setTrafficLights: (lights: TrafficLight[]) => void;
  updateTrafficLight: (id: string, updates: Partial<TrafficLight>) => void;
  setMetrics: (metrics: SimulationMetrics) => void;
  setScenarios: (scenarios: Scenario[]) => void;
  setCurrentScenario: (scenario: Scenario | null) => void;
  reset: () => void;
}

const initialState: SimulationState = {
  isRunning: false,
  isPaused: false,
  currentScenario: null,
  simulationTime: 0,
  speedMultiplier: 1,
  optimizationMode: false,
};

export const useSimulationStore = create<SimulationStore>((set) => ({
  state: initialState,
  vehicles: new Map(),
  trafficLights: new Map(),
  metrics: null,
  scenarios: [],
  currentScenario: null,

  setState: (newState) =>
    set((state) => ({
      state: { ...state.state, ...newState },
    })),

  setVehicles: (vehicles) =>
    set(() => ({
      vehicles: new Map(vehicles.map((v) => [v.id, v])),
    })),

  updateVehicle: (id, updates) =>
    set((state) => {
      const newVehicles = new Map(state.vehicles);
      const vehicle = newVehicles.get(id);
      if (vehicle) {
        newVehicles.set(id, { ...vehicle, ...updates });
      }
      return { vehicles: newVehicles };
    }),

  removeVehicle: (id) =>
    set((state) => {
      const newVehicles = new Map(state.vehicles);
      newVehicles.delete(id);
      return { vehicles: newVehicles };
    }),

  setTrafficLights: (lights) =>
    set(() => ({
      trafficLights: new Map(lights.map((l) => [l.id, l])),
    })),

  updateTrafficLight: (id, updates) =>
    set((state) => {
      const newLights = new Map(state.trafficLights);
      const light = newLights.get(id);
      if (light) {
        newLights.set(id, { ...light, ...updates });
      }
      return { trafficLights: newLights };
    }),

  setMetrics: (metrics) => set({ metrics }),

  setScenarios: (scenarios) => set({ scenarios }),

  setCurrentScenario: (scenario) =>
    set((state) => ({
      currentScenario: scenario,
      state: { ...state.state, currentScenario: scenario?.id || null },
    })),

  reset: () =>
    set({
      state: initialState,
      vehicles: new Map(),
      trafficLights: new Map(),
      metrics: null,
      currentScenario: null,
    }),
}));
