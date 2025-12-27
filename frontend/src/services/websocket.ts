import { io, Socket } from 'socket.io-client';
import {
  WebSocketMessage,
  Vehicle,
  TrafficLight,
  SimulationMetrics,
  VehicleUpdate,
  TrafficLightUpdate,
} from '../types';
import { WS_EVENTS } from '../utils/constants';

type EventCallback = (data: unknown) => void;

class WebSocketService {
  private socket: Socket | null = null;
  private mockMode: boolean = true;
  private mockInterval: NodeJS.Timeout | null = null;
  private eventHandlers: Map<string, Set<EventCallback>> = new Map();

  connect(url?: string): void {
    if (this.socket?.connected) {
      return;
    }

    const wsUrl = url || import.meta.env.VITE_WS_URL || 'ws://localhost:5000';

    if (this.mockMode) {
      this.startMockUpdates();
      this.triggerEvent(WS_EVENTS.CONNECT, null);
    } else {
      this.socket = io(wsUrl, {
        transports: ['websocket'],
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionAttempts: 5,
      });

      this.socket.on(WS_EVENTS.CONNECT, () => {
        this.triggerEvent(WS_EVENTS.CONNECT, null);
      });

      this.socket.on(WS_EVENTS.DISCONNECT, () => {
        this.triggerEvent(WS_EVENTS.DISCONNECT, null);
      });

      Object.values(WS_EVENTS).forEach((event) => {
        this.socket?.on(event, (data: unknown) => {
          this.triggerEvent(event, data);
        });
      });
    }
  }

  disconnect(): void {
    if (this.mockInterval) {
      clearInterval(this.mockInterval);
      this.mockInterval = null;
    }

    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }

    this.triggerEvent(WS_EVENTS.DISCONNECT, null);
  }

  on(event: string, callback: EventCallback): void {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, new Set());
    }
    this.eventHandlers.get(event)?.add(callback);
  }

  off(event: string, callback: EventCallback): void {
    this.eventHandlers.get(event)?.delete(callback);
  }

  private triggerEvent(event: string, data: unknown): void {
    const handlers = this.eventHandlers.get(event);
    if (handlers) {
      handlers.forEach((handler) => handler(data));
    }
  }

  private startMockUpdates(): void {
    const mockVehicles = this.generateMockVehicles(20);
    const mockTrafficLights = this.generateMockTrafficLights(10);

    this.mockInterval = setInterval(() => {
      const vehicleUpdates: VehicleUpdate[] = mockVehicles.map((v) => ({
        id: v.id,
        position: {
          lat: v.position.lat + (Math.random() - 0.5) * 0.001,
          lng: v.position.lng + (Math.random() - 0.5) * 0.001,
        },
        speed: Math.max(0, v.speed + (Math.random() - 0.5) * 10),
        angle: Math.random() * 360,
        timestamp: Date.now(),
      }));

      mockVehicles.forEach((v, i) => {
        v.position = vehicleUpdates[i].position;
        v.speed = vehicleUpdates[i].speed;
      });

      this.triggerEvent(WS_EVENTS.VEHICLE_UPDATE, { updates: vehicleUpdates });

      if (Math.random() > 0.7) {
        const lightUpdates: TrafficLightUpdate[] = mockTrafficLights.map((l) => ({
          id: l.id,
          state: this.randomTrafficLightState(),
          currentPhase: Math.floor(Math.random() * 4),
          remainingDuration: Math.floor(Math.random() * 30) + 10,
          timestamp: Date.now(),
        }));

        this.triggerEvent(WS_EVENTS.TRAFFIC_LIGHT_UPDATE, { updates: lightUpdates });
      }

      const metrics: SimulationMetrics = {
        timestamp: new Date().toISOString(),
        totalVehicles: mockVehicles.length,
        avgSpeed: mockVehicles.reduce((sum, v) => sum + v.speed, 0) / mockVehicles.length,
        avgTravelTime: 120 + Math.random() * 60,
        co2Emissions: 50 + Math.random() * 20,
        queueLengths: {
          'junction-1': Math.floor(Math.random() * 10),
          'junction-2': Math.floor(Math.random() * 10),
          'junction-3': Math.floor(Math.random() * 10),
        },
        emergencyVehiclesActive: mockVehicles.filter((v) => v.type === 'emergency').length,
        completedTrips: Math.floor(Math.random() * 100),
        waitingTime: 30 + Math.random() * 20,
      };

      this.triggerEvent(WS_EVENTS.METRICS_UPDATE, { metrics });
    }, 1000);

    this.triggerEvent(WS_EVENTS.SIMULATION_UPDATE, {
      simulationTime: 0,
      vehicles: mockVehicles,
      trafficLights: mockTrafficLights,
      metrics: null,
      state: {
        isRunning: true,
        isPaused: false,
        currentScenario: 'scenario-1',
        simulationTime: 0,
        speedMultiplier: 1,
        optimizationMode: false,
      },
    });
  }

  private generateMockVehicles(count: number): Vehicle[] {
    const types: Vehicle['type'][] = ['passenger', 'bus', 'truck', 'emergency'];
    const basePosition = { lat: 48.8566, lng: 2.3522 };

    return Array.from({ length: count }, (_, i) => ({
      id: `vehicle-${i}`,
      type: types[Math.floor(Math.random() * types.length)],
      position: {
        lat: basePosition.lat + (Math.random() - 0.5) * 0.02,
        lng: basePosition.lng + (Math.random() - 0.5) * 0.02,
      },
      speed: Math.random() * 60,
      lane: `lane-${Math.floor(Math.random() * 3)}`,
      route: [`edge-${Math.floor(Math.random() * 10)}`],
      angle: Math.random() * 360,
    }));
  }

  private generateMockTrafficLights(count: number): TrafficLight[] {
    const basePosition = { lat: 48.8566, lng: 2.3522 };

    return Array.from({ length: count }, (_, i) => ({
      id: `tl-${i}`,
      position: {
        lat: basePosition.lat + (Math.random() - 0.5) * 0.02,
        lng: basePosition.lng + (Math.random() - 0.5) * 0.02,
      },
      state: this.randomTrafficLightState(),
      currentPhase: Math.floor(Math.random() * 4),
      phases: [
        { duration: 30, state: 'GGGrrr' },
        { duration: 3, state: 'yyyrrr' },
        { duration: 30, state: 'rrrGGG' },
        { duration: 3, state: 'rrryyy' },
      ],
      remainingDuration: Math.floor(Math.random() * 30),
    }));
  }

  private randomTrafficLightState(): string {
    const states = ['GGGrrr', 'yyyrrr', 'rrrGGG', 'rrryyy'];
    return states[Math.floor(Math.random() * states.length)];
  }

  setMockMode(enabled: boolean): void {
    this.mockMode = enabled;
  }

  isConnected(): boolean {
    if (this.mockMode) {
      return this.mockInterval !== null;
    }
    return this.socket?.connected ?? false;
  }
}

export const websocketService = new WebSocketService();
