import { useEffect, useState, useRef } from 'react';
import { websocketService } from '../services/websocket';
import { WS_EVENTS } from '../utils/constants';
import { useSimulationStore } from '../stores';
import {
  SimulationUpdateData,
  VehicleUpdateData,
  TrafficLightUpdateData,
  MetricsUpdateData,
} from '../types';

export const useWebSocket = () => {
  // Utilisez les fonctions du store de manière directe, pas dans des callbacks
  const setVehicles = useSimulationStore((state) => state.setVehicles);
  const updateVehicle = useSimulationStore((state) => state.updateVehicle);
  const setTrafficLights = useSimulationStore((state) => state.setTrafficLights);
  const updateTrafficLight = useSimulationStore((state) => state.updateTrafficLight);
  const setMetrics = useSimulationStore((state) => state.setMetrics);
  
  const [isConnected, setIsConnected] = useState(false);
  
  // Références pour éviter les dépendances changeantes
  const handlersRef = useRef({
    setVehicles,
    updateVehicle,
    setTrafficLights,
    updateTrafficLight,
    setMetrics,
  });

  // Mettez à jour les références quand les fonctions changent
  useEffect(() => {
    handlersRef.current = {
      setVehicles,
      updateVehicle,
      setTrafficLights,
      updateTrafficLight,
      setMetrics,
    };
  }, [setVehicles, updateVehicle, setTrafficLights, updateTrafficLight, setMetrics]);

  useEffect(() => {
    console.log('Setting up WebSocket connection...');
    
    const handleConnect = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    const handleDisconnect = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    const handleSimulationUpdate = (data: SimulationUpdateData) => {
      console.log('Received simulation update:', data);
      if (data.vehicles) {
        handlersRef.current.setVehicles(data.vehicles);
      }
      if (data.trafficLights) {
        handlersRef.current.setTrafficLights(data.trafficLights);
      }
      if (data.metrics) {
        handlersRef.current.setMetrics(data.metrics);
      }
    };

    const handleVehicleUpdate = (data: VehicleUpdateData) => {
      data.updates.forEach((update) => {
        handlersRef.current.updateVehicle(update.id, {
          position: update.position,
          speed: update.speed,
          angle: update.angle,
        });
      });
    };

    const handleTrafficLightUpdate = (data: TrafficLightUpdateData) => {
      data.updates.forEach((update) => {
        handlersRef.current.updateTrafficLight(update.id, {
          state: update.state,
          currentPhase: update.currentPhase,
          remainingDuration: update.remainingDuration,
        });
      });
    };

    const handleMetricsUpdate = (data: MetricsUpdateData) => {
      handlersRef.current.setMetrics(data.metrics);
    };

    // Connectez-vous d'abord
    websocketService.connect();
    setIsConnected(websocketService.isConnected());

    // Configurez les listeners
    websocketService.on(WS_EVENTS.CONNECT, handleConnect);
    websocketService.on(WS_EVENTS.DISCONNECT, handleDisconnect);
    websocketService.on(WS_EVENTS.SIMULATION_UPDATE, handleSimulationUpdate);
    websocketService.on(WS_EVENTS.VEHICLE_UPDATE, handleVehicleUpdate);
    websocketService.on(WS_EVENTS.TRAFFIC_LIGHT_UPDATE, handleTrafficLightUpdate);
    websocketService.on(WS_EVENTS.METRICS_UPDATE, handleMetricsUpdate);

    // Cleanup
    return () => {
      console.log('Cleaning up WebSocket...');
      websocketService.off(WS_EVENTS.CONNECT, handleConnect);
      websocketService.off(WS_EVENTS.DISCONNECT, handleDisconnect);
      websocketService.off(WS_EVENTS.SIMULATION_UPDATE, handleSimulationUpdate);
      websocketService.off(WS_EVENTS.VEHICLE_UPDATE, handleVehicleUpdate);
      websocketService.off(WS_EVENTS.TRAFFIC_LIGHT_UPDATE, handleTrafficLightUpdate);
      websocketService.off(WS_EVENTS.METRICS_UPDATE, handleMetricsUpdate);
      
      // Ne déconnectez pas automatiquement si vous voulez garder la connexion
      // websocketService.disconnect();
    };
  }, []); // Tableau de dépendances VIDE - ne dépend d'aucune fonction

  return {
    connect: () => websocketService.connect(),
    disconnect: () => websocketService.disconnect(),
    isConnected,
  };
};