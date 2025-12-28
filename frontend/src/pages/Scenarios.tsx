import { useEffect, useState } from 'react';
import { Card, Button, Badge } from '../components/common';
import { scenariosAPI, Scenario } from '../services/api';
import { Play, Users, Clock, AlertTriangle } from 'lucide-react';
import { useSimulation } from '../hooks/useSimulation';

export const Scenarios = () => {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const { startSimulation } = useSimulation();

  useEffect(() => {
    loadScenarios();
  }, []);

  const loadScenarios = async () => {
    const data = await scenariosAPI.getAll();
    setScenarios(data.scenarios);
  };

  const handleRunScenario = (scenarioId: string) => {
    startSimulation({ scenarioId });
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Scenarios</h1>
        <p className="text-gray-600 mt-2">Manage and run traffic simulation scenarios</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {scenarios.map((scenario) => (
          <Card key={scenario.id} padding="md">
            <div className="space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{scenario.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{scenario.description}</p>
                </div>
                {scenario.trafficDensity === 'high' && (
                  <Badge variant="warning">Rush Hour</Badge>
                )}
              </div>

              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="flex items-center space-x-2 text-gray-700">
                  <Users className="w-4 h-4" />
                  <span>{scenario.vehicleCount} vehicles</span>
                </div>
                <div className="flex items-center space-x-2 text-gray-700">
                  <Clock className="w-4 h-4" />
                  <span>{scenario.duration / 60} min</span>
                </div>
                {scenario.hasEmergencyVehicles && (
                  <div className="flex items-center space-x-2 text-gray-700">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Emergency vehicles</span>
                  </div>
                )}
              </div>

              <Button
                variant="primary"
                className="w-full"
                onClick={() => handleRunScenario(scenario.id)}
              >
                <Play className="w-4 h-4 mr-2" />
                Run Scenario
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
