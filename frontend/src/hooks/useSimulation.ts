import { useCallback } from 'react';
import { simulationAPI, vehiclesAPI } from '../services/api.ts';
import { useSimulationStore } from '../stores';
import { useUIStore } from '../stores';
import { StartSimulationRequest, EmergencyVehicleRequest } from '../types';

export const useSimulation = () => {
  const { state, setState, reset, setCurrentScenario } = useSimulationStore();
  const { addAlert, setLoading } = useUIStore();

  const startSimulation = useCallback(
    async (request: StartSimulationRequest) => {
      try {
        setLoading(true, 'Starting simulation...');
        const scenarioId = request.scenarioId || 'default';
        const response = await simulationAPI.start(scenarioId);

        setState({ 
          isRunning: true, 
          isPaused: false,
          currentScenario: scenarioId,
          speedMultiplier: request.speedMultiplier || 1,
          optimizationMode: request.optimizationMode || false,
        });
        addAlert({
          type: 'success',
          message: response.message || 'Simulation started',
          duration: 3000,
        });
      } catch (error) {
        addAlert({
          type: 'error',
          message: 'Failed to start simulation',
          duration: 5000,
        });
      } finally {
        setLoading(false);
      }
    },
    [setState, addAlert, setLoading]
  );

  const stopSimulation = useCallback(async () => {
    try {
      setLoading(true, 'Stopping simulation...');
      const response = await simulationAPI.stop();

      setState({ isRunning: false, isPaused: false });
      addAlert({
        type: 'success',
        message: response.message || 'Simulation stopped',
        duration: 3000,
      });
    } catch (error) {
      addAlert({
        type: 'error',
        message: 'Failed to stop simulation',
        duration: 5000,
      });
    } finally {
      setLoading(false);
    }
  }, [setState, addAlert, setLoading]);

  const pauseSimulation = useCallback(async () => {
    try {
      const response = await simulationAPI.pause();
      setState({ isPaused: true });
      addAlert({
        type: 'info',
        message: response.message || 'Simulation paused',
        duration: 2000,
      });
    } catch (error) {
      addAlert({
        type: 'error',
        message: 'Failed to pause simulation',
        duration: 5000,
      });
    }
  }, [setState, addAlert]);

  const resumeSimulation = useCallback(async () => {
    try {
      const response = await simulationAPI.resume();
      setState({ isPaused: false });
      addAlert({
        type: 'info',
        message: response.message || 'Simulation resumed',
        duration: 2000,
      });
    } catch (error) {
      addAlert({
        type: 'error',
        message: 'Failed to resume simulation',
        duration: 5000,
      });
    }
  }, [setState, addAlert]);

  const resetSimulation = useCallback(() => {
    reset();
    addAlert({
      type: 'info',
      message: 'Simulation reset',
      duration: 2000,
    });
  }, [reset, addAlert]);

  const setSpeedMultiplier = useCallback(
    (speed: number) => {
      setState({ speedMultiplier: speed });
      addAlert({
        type: 'info',
        message: `Speed set to ${speed}x`,
        duration: 2000,
      });
    },
    [setState, addAlert]
  );

  const toggleOptimization = useCallback(() => {
    setState({ optimizationMode: !state.optimizationMode });
    addAlert({
      type: 'info',
      message: `Optimization ${!state.optimizationMode ? 'enabled' : 'disabled'}`,
      duration: 2000,
    });
  }, [state.optimizationMode, setState, addAlert]);

  const addEmergencyVehicle = useCallback(
    async (_request: EmergencyVehicleRequest) => {
      try {
        const response = await vehiclesAPI.addEmergency();
        addAlert({
          type: 'success',
          message: response.message || 'Emergency vehicle dispatched',
          duration: 3000,
        });
      } catch (error) {
        addAlert({
          type: 'error',
          message: 'Failed to add emergency vehicle',
          duration: 5000,
        });
      }
    },
    [addAlert]
  );

  return {
    state,
    startSimulation,
    stopSimulation,
    pauseSimulation,
    resumeSimulation,
    resetSimulation,
    setSpeedMultiplier,
    toggleOptimization,
    addEmergencyVehicle,
    setCurrentScenario,
  };
};
