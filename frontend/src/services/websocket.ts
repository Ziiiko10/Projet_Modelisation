/**
 * Service WebSocket pour Urban Flow
 */

const WS_URL = 'ws://localhost:5000/ws';

// Types d'événements
export type WebSocketEvent =
  | 'simulation_update'
  | 'vehicle_update'
  | 'traffic_light_update'
  | 'metrics_update'
  | 'simulation_status'
  | 'notification'
  | 'emergency_alert'
  | 'error'
  | 'connect';

export interface WebSocketMessage {
  type: WebSocketEvent;
  data: any;
  timestamp?: string;
}

export interface SimulationUpdate {
  vehicles: any[];
  traffic_lights: any[];
  metrics: any;
  simulation_time: number;
  scenario: string;
}

export interface VehicleUpdate {
  vehicles: any[];
  count: number;
}

export interface MetricsUpdate {
  metrics: any;
}

export interface SimulationStatusUpdate {
  status: 'stopped' | 'running' | 'paused';
  current_scenario?: string;
  simulation_time?: number;
  message?: string;
}

class WebSocketService {
  private socket: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 3000;
  private eventListeners: Map<WebSocketEvent, Function[]> = new Map();
  private isConnected = false;
  private connectionPromise: Promise<void> | null = null;

  constructor() {
    this.connect();
  }

  // Connexion au WebSocket
  connect(): Promise<void> {
    if (this.connectionPromise) {
      return this.connectionPromise;
    }

    this.connectionPromise = new Promise((resolve, reject) => {
      try {
        this.socket = new WebSocket(WS_URL);

        this.socket.onopen = () => {
          console.log('✅ WebSocket connected to:', WS_URL);
          this.isConnected = true;
          this.reconnectAttempts = 0;
          this.emit('connect', { message: 'Connected' });
          resolve();
        };

        this.socket.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            this.handleMessage(message);
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        this.socket.onclose = () => {
          console.log('❌ WebSocket disconnected');
          this.isConnected = false;
          this.socket = null;
          this.connectionPromise = null;
          this.attemptReconnect();
        };

        this.socket.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        };
      } catch (error) {
        reject(error);
      }
    });

    return this.connectionPromise;
  }

  // Tentative de reconnexion
  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * this.reconnectAttempts;

    console.log(`Attempting to reconnect in ${delay}ms... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

    setTimeout(() => {
      if (!this.isConnected) {
        this.connect();
      }
    }, delay);
  }

  // Gestion des messages
  private handleMessage(message: WebSocketMessage) {
    const { type, data, timestamp } = message;
    
    // Émettre l'événement
    this.emit(type, data);

    // Log pour le débogage
    if (type !== 'simulation_update' && type !== 'vehicle_update') {
      console.log(`📨 WebSocket [${type}]:`, data);
    }
  }

  // Émettre un événement
  private emit(event: WebSocketEvent, data: any) {
    const listeners = this.eventListeners.get(event);
    if (listeners) {
      listeners.forEach(listener => {
        try {
          listener(data);
        } catch (error) {
          console.error(`Error in event listener for ${event}:`, error);
        }
      });
    }
  }

  // Écouter un événement
  on(event: WebSocketEvent, callback: (data: any) => void): () => void {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    
    const listeners = this.eventListeners.get(event)!;
    listeners.push(callback);

    // Retourner une fonction pour supprimer l'écouteur
    return () => {
      const index = listeners.indexOf(callback);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    };
  }

  // Envoyer une commande
  sendCommand(command: string, data?: any): void {
    if (!this.isConnected || !this.socket) {
      console.error('Cannot send command: WebSocket not connected');
      return;
    }

    const message = {
      command,
      ...data,
    };

    try {
      this.socket.send(JSON.stringify(message));
      console.log(`📤 Sent command: ${command}`, data || '');
    } catch (error) {
      console.error('Error sending command:', error);
    }
  }

  // Commandes de simulation
  startSimulation(scenarioId: string = 'default') {
    this.sendCommand('start', { scenario_id: scenarioId });
  }

  pauseSimulation() {
    this.sendCommand('pause');
  }

  resumeSimulation() {
    this.sendCommand('resume');
  }

  stopSimulation() {
    this.sendCommand('stop');
  }

  resetSimulation() {
    this.sendCommand('reset');
  }

  addEmergencyVehicle() {
    this.sendCommand('emergency_vehicle');
  }

  changeScenario(scenarioId: string) {
    this.sendCommand('change_scenario', { scenario_id: scenarioId });
  }

  getStatus() {
    this.sendCommand('get_status');
  }

  // Statut de connexion
  isConnectedState(): boolean {
    return this.isConnected;
  }

  // Déconnexion
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
      this.isConnected = false;
      this.connectionPromise = null;
    }
  }
}

// Instance singleton
export const websocketService = new WebSocketService();

export default websocketService;