/**
 * Service API REST pour Urban Flow
 */

const API_BASE_URL = 'http://localhost:5000/api';

// Types de base
export interface Scenario {
  id: string;
  name: string;
  description: string;
  vehicleCount: number;
  trafficDensity: string;
  hasEmergencyVehicles: boolean;
  duration: number;
  isActive: boolean;
}

export interface Vehicle {
  id: string;
  type: string;
  position: { lat: number; lng: number };
  speed: number;
  lane: string;
  route: string[];
  color: string;
  heading: number;
}

export interface Metrics {
  timestamp: string;
  totalVehicles: number;
  avgSpeed: number;
  avgTravelTime: number;
  co2Emissions: number;
  emergencyVehiclesActive: number;
  throughput: number;
  congestionLevel: string;
}

export interface SimulationStatus {
  status: 'stopped' | 'running' | 'paused';
  currentScenario: string | null;
  startTime: string | null;
  elapsedTime: number;
  totalVehicles: number;
}

// Fonctions utilitaires
async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
}

// API des scénarios
export const scenariosAPI = {
  // Récupérer tous les scénarios
  getAll: async (): Promise<{ scenarios: Scenario[] }> => {
    return fetchAPI('/scenarios');
  },

  // Récupérer un scénario spécifique
  getById: async (id: string): Promise<Scenario> => {
    return fetchAPI(`/scenarios/${id}`);
  },

  // Activer un scénario
  activate: async (id: string): Promise<{ message: string; scenario: Scenario }> => {
    return fetchAPI(`/scenarios/${id}/activate`, {
      method: 'POST',
    });
  },

  // Créer un nouveau scénario
  create: async (scenario: Omit<Scenario, 'isActive'>): Promise<{ message: string; scenario: Scenario }> => {
    return fetchAPI('/scenarios', {
      method: 'POST',
      body: JSON.stringify(scenario),
    });
  },
};

// API de simulation
export const simulationAPI = {
  // Récupérer l'état de la simulation
  getStatus: async (): Promise<SimulationStatus> => {
    return fetchAPI('/simulation/status');
  },

  // Démarrer la simulation
  start: async (scenarioId: string = 'default'): Promise<{ message: string; status: string }> => {
    return fetchAPI('/simulation/start', {
      method: 'POST',
      body: JSON.stringify({ scenario_id: scenarioId }),
    });
  },

  // Mettre en pause
  pause: async (): Promise<{ message: string }> => {
    return fetchAPI('/simulation/pause', {
      method: 'POST',
    });
  },

  // Reprendre
  resume: async (): Promise<{ message: string }> => {
    return fetchAPI('/simulation/resume', {
      method: 'POST',
    });
  },

  // Arrêter
  stop: async (): Promise<{ message: string }> => {
    return fetchAPI('/simulation/stop', {
      method: 'POST',
    });
  },

  // Réinitialiser
  reset: async (): Promise<{ message: string }> => {
    return fetchAPI('/simulation/reset', {
      method: 'POST',
    });
  },
};

// API des véhicules
export const vehiclesAPI = {
  // Récupérer tous les véhicules
  getAll: async (): Promise<{ vehicles: Vehicle[]; count: number }> => {
    return fetchAPI('/vehicles');
  },

  // Ajouter un véhicule d'urgence
  addEmergency: async (): Promise<{ message: string; vehicle: Vehicle }> => {
    return fetchAPI('/vehicles/emergency', {
      method: 'POST',
    });
  },

  // Supprimer un véhicule
  remove: async (id: string): Promise<{ message: string }> => {
    return fetchAPI(`/vehicles/${id}`, {
      method: 'DELETE',
    });
  },
};

// API des métriques
export const metricsAPI = {
  // Récupérer les métriques actuelles
  getCurrent: async (): Promise<Metrics> => {
    return fetchAPI('/metrics');
  },

  // Récupérer l'historique
  getHistory: async (): Promise<{ metrics: Metrics[] }> => {
    return fetchAPI('/metrics/history');
  },

  // Récupérer le résumé
  getSummary: async (): Promise<any> => {
    return fetchAPI('/metrics/summary');
  },
};

// API de santé
export const healthAPI = {
  // Vérifier la santé du backend
  check: async (): Promise<{ status: string; services: any }> => {
    return fetchAPI('/health');
  },

  // Version du backend
  getVersion: async (): Promise<{ version: string; api: string }> => {
    return fetchAPI('/version');
  },
};

// Fonction de test de connexion
export const testConnection = async (): Promise<boolean> => {
  try {
    const health = await healthAPI.check();
    return health.status === 'healthy';
  } catch (error) {
    console.error('Backend connection failed:', error);
    return false;
  }
};

export default {
  scenarios: scenariosAPI,
  simulation: simulationAPI,
  vehicles: vehiclesAPI,
  metrics: metricsAPI,
  health: healthAPI,
  testConnection,
};