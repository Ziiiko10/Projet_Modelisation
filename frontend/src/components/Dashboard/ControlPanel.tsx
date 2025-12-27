import { Play, Pause, Square, RotateCcw, Zap } from 'lucide-react';
import { Card, Button, Badge } from '../common';
import { useSimulation } from '../../hooks/useSimulation';
import { SIMULATION_SPEED_OPTIONS } from '../../utils/constants';

export const ControlPanel = () => {
  const {
    state,
    startSimulation,
    stopSimulation,
    pauseSimulation,
    resumeSimulation,
    resetSimulation,
    setSpeedMultiplier,
    toggleOptimization,
  } = useSimulation();

  const handleStartStop = () => {
    if (state.isRunning) {
      if (state.isPaused) {
        resumeSimulation();
      } else {
        pauseSimulation();
      }
    } else {
      startSimulation({ scenarioId: 'scenario-1' });
    }
  };

  return (
    <Card padding="md" title="Simulation Controls">
      <div className="space-y-4 mt-4">
        <div className="flex items-center space-x-2">
          <Button
            variant={state.isRunning && !state.isPaused ? 'secondary' : 'primary'}
            onClick={handleStartStop}
            className="flex-1"
          >
            {state.isRunning && !state.isPaused ? (
              <>
                <Pause className="w-4 h-4 mr-2" />
                Pause
              </>
            ) : (
              <>
                <Play className="w-4 h-4 mr-2" />
                {state.isPaused ? 'Resume' : 'Start'}
              </>
            )}
          </Button>

          <Button variant="danger" onClick={stopSimulation} disabled={!state.isRunning}>
            <Square className="w-4 h-4 mr-2" />
            Stop
          </Button>

          <Button variant="ghost" onClick={resetSimulation}>
            <RotateCcw className="w-4 h-4" />
          </Button>
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm font-medium text-gray-700">Speed Multiplier</label>
            <Badge variant="info">{state.speedMultiplier}x</Badge>
          </div>
          <div className="flex space-x-2">
            {SIMULATION_SPEED_OPTIONS.map((speed) => (
              <button
                key={speed}
                onClick={() => setSpeedMultiplier(speed)}
                disabled={!state.isRunning}
                className={`flex-1 px-3 py-2 text-sm rounded transition-colors ${
                  state.speedMultiplier === speed
                    ? 'bg-primary-100 text-primary-700 font-medium'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200 disabled:opacity-50'
                }`}
              >
                {speed}x
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <label className="text-sm font-medium text-gray-700">Optimization Mode</label>
            <p className="text-xs text-gray-500">AI-powered traffic optimization</p>
          </div>
          <button
            onClick={toggleOptimization}
            disabled={!state.isRunning}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
              state.optimizationMode ? 'bg-green-600' : 'bg-gray-300'
            } disabled:opacity-50`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                state.optimizationMode ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
        </div>

        {state.isRunning && (
          <div className="pt-4 border-t border-gray-200">
            <div className="flex items-center space-x-2 text-sm">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-gray-700">
                Simulation running - {Math.floor(state.simulationTime)}s
              </span>
            </div>
          </div>
        )}
      </div>
    </Card>
  );
};
