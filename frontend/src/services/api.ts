import axios from 'axios';
import {
  ApiResponse,
  Scenario,
  SimulationState,
  SimulationMetrics,
  StartSimulationRequest,
  EmergencyVehicleRequest,
} from '../types';
import { API_ENDPOINTS } from '../utils/constants';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const scenariosApi = {
  getAll: async (): Promise<Scenario[]> => {
    const mockScenarios: Scenario[] = [
      {
        id: 'scenario-1',
        name: 'Rush Hour',
        description: 'High traffic volume during peak hours',
        vehicleCount: 500,
        duration: 3600,
        emergencyVehicles: 5,
        rushHourMode: true,
        createdAt: new Date().toISOString(),
      },
      {
        id: 'scenario-2',
        name: 'Normal Traffic',
        description: 'Standard traffic conditions',
        vehicleCount: 200,
        duration: 3600,
        emergencyVehicles: 2,
        rushHourMode: false,
        createdAt: new Date().toISOString(),
      },
      {
        id: 'scenario-3',
        name: 'Emergency Response',
        description: 'Multiple emergency vehicles active',
        vehicleCount: 150,
        duration: 1800,
        emergencyVehicles: 10,
        rushHourMode: false,
        createdAt: new Date().toISOString(),
      },
    ];

    return mockScenarios;
  },

  getById: async (id: string): Promise<Scenario | null> => {
    const scenarios = await scenariosApi.getAll();
    return scenarios.find((s) => s.id === id) || null;
  },

  create: async (scenario: Omit<Scenario, 'id' | 'createdAt'>): Promise<Scenario> => {
    const newScenario: Scenario = {
      ...scenario,
      id: `scenario-${Date.now()}`,
      createdAt: new Date().toISOString(),
    };
    return newScenario;
  },
};

export const simulationApi = {
  start: async (request: StartSimulationRequest): Promise<ApiResponse<SimulationState>> => {
    return {
      success: true,
      data: {
        isRunning: true,
        isPaused: false,
        currentScenario: request.scenarioId || null,
        simulationTime: 0,
        speedMultiplier: request.speedMultiplier || 1,
        optimizationMode: request.optimizationMode || false,
      },
      message: 'Simulation started successfully',
    };
  },

  stop: async (): Promise<ApiResponse<void>> => {
    return {
      success: true,
      message: 'Simulation stopped successfully',
    };
  },

  pause: async (): Promise<ApiResponse<void>> => {
    return {
      success: true,
      message: 'Simulation paused',
    };
  },

  resume: async (): Promise<ApiResponse<void>> => {
    return {
      success: true,
      message: 'Simulation resumed',
    };
  },

  getStatus: async (): Promise<SimulationState> => {
    return {
      isRunning: false,
      isPaused: false,
      currentScenario: null,
      simulationTime: 0,
      speedMultiplier: 1,
      optimizationMode: false,
    };
  },

  getMetrics: async (): Promise<SimulationMetrics> => {
    return {
      timestamp: new Date().toISOString(),
      totalVehicles: 0,
      avgSpeed: 0,
      avgTravelTime: 0,
      co2Emissions: 0,
      queueLengths: {},
      emergencyVehiclesActive: 0,
      completedTrips: 0,
      waitingTime: 0,
    };
  },

  addEmergencyVehicle: async (
    request: EmergencyVehicleRequest
  ): Promise<ApiResponse<void>> => {
    return {
      success: true,
      message: 'Emergency vehicle added successfully',
    };
  },
};
