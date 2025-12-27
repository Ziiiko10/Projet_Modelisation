import React, { useState, useEffect } from 'react';
import apiService, { testConnection } from '../services/api';
import websocketService from '../services/websocket';

const ConnectionTest: React.FC = () => {
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'error'>('checking');
  const [websocketStatus, setWebsocketStatus] = useState<'disconnected' | 'connected'>('disconnected');
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [simulationStatus, setSimulationStatus] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [log, setLog] = useState<string[]>([]);

  const addLog = (message: string) => {
    setLog(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  // Tester la connexion au backend
  const testBackendConnection = async () => {
    setBackendStatus('checking');
    addLog('Testing backend connection...');
    
    try {
      const isConnected = await testConnection();
      
      if (isConnected) {
        setBackendStatus('connected');
        addLog('✅ Backend connected successfully!');
        
        // Récupérer les scénarios
        const scenariosData = await apiService.scenarios.getAll();
        setScenarios(scenariosData.scenarios);
        addLog(`📊 Loaded ${scenariosData.scenarios.length} scenarios`);
        
        // Récupérer le statut de simulation
        const status = await apiService.simulation.getStatus();
        setSimulationStatus(status);
        addLog(`🔄 Simulation status: ${status.status}`);
        
        // Récupérer les métriques
        const metricsData = await apiService.metrics.getCurrent();
        setMetrics(metricsData);
        addLog('📈 Metrics loaded');
        
      } else {
        setBackendStatus('error');
        addLog('❌ Backend connection failed');
      }
    } catch (error) {
      setBackendStatus('error');
      addLog(`❌ Error: ${error}`);
    }
  };

  // Configurer WebSocket
  useEffect(() => {
    // Écouter les événements WebSocket
    const removeSimulationUpdate = websocketService.on('simulation_update', (data) => {
      addLog('🔄 Simulation update received');
    });

    const removeVehicleUpdate = websocketService.on('vehicle_update', (data) => {
      addLog(`🚗 ${data.count} vehicles updated`);
    });

    const removeMetricsUpdate = websocketService.on('metrics_update', (data) => {
      setMetrics(data.metrics);
      addLog('📈 Metrics updated');
    });

    const removeSimulationStatus = websocketService.on('simulation_status', (data) => {
      setSimulationStatus(data);
      addLog(`🔄 Simulation status: ${data.status}`);
    });

    const removeConnect = websocketService.on('connect', () => {
      setWebsocketStatus('connected');
      addLog('✅ WebSocket connected');
    });

    const removeNotification = websocketService.on('notification', (data) => {
      addLog(`📢 ${data.message}`);
    });

    // Tester la connexion initiale
    testBackendConnection();

    return () => {
      removeSimulationUpdate();
      removeVehicleUpdate();
      removeMetricsUpdate();
      removeSimulationStatus();
      removeConnect();
      removeNotification();
    };
  }, []);

  // Commander la simulation
  const startSimulation = async () => {
    addLog('Starting simulation...');
    try {
      await apiService.simulation.start('default');
      addLog('Simulation started');
    } catch (error) {
      addLog(`Error: ${error}`);
    }
  };

  const addEmergencyVehicle = async () => {
    addLog('Adding emergency vehicle...');
    try {
      await apiService.vehicles.addEmergency();
      addLog('Emergency vehicle added');
    } catch (error) {
      addLog(`Error: ${error}`);
    }
  };

  return (
    <div style={{
      padding: '20px',
      fontFamily: 'Arial, sans-serif',
      maxWidth: '800px',
      margin: '0 auto'
    }}>
      <h1>Urban Flow - Connection Test</h1>
      
      {/* Status */}
      <div style={{ marginBottom: '20px' }}>
        <h2>Connection Status</h2>
        <div style={{ display: 'flex', gap: '20px' }}>
          <div>
            <strong>Backend REST API:</strong>{' '}
            <span style={{
              color: backendStatus === 'connected' ? 'green' : 
                     backendStatus === 'error' ? 'red' : 'orange'
            }}>
              {backendStatus === 'connected' ? '✅ Connected' : 
               backendStatus === 'error' ? '❌ Error' : '⏳ Checking...'}
            </span>
          </div>
          <div>
            <strong>WebSocket:</strong>{' '}
            <span style={{
              color: websocketStatus === 'connected' ? 'green' : 'red'
            }}>
              {websocketStatus === 'connected' ? '✅ Connected' : '❌ Disconnected'}
            </span>
          </div>
        </div>
      </div>

      {/* Controls */}
      <div style={{ marginBottom: '20px' }}>
        <h2>Controls</h2>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button 
            onClick={testBackendConnection}
            style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px' }}
          >
            Test Connection
          </button>
          <button 
            onClick={startSimulation}
            style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '5px' }}
          >
            Start Simulation
          </button>
          <button 
            onClick={addEmergencyVehicle}
            style={{ padding: '10px 20px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '5px' }}
          >
            Add Emergency Vehicle
          </button>
          <button 
            onClick={() => websocketService.stopSimulation()}
            style={{ padding: '10px 20px', backgroundColor: '#ffc107', color: 'black', border: 'none', borderRadius: '5px' }}
          >
            Stop Simulation
          </button>
        </div>
      </div>

      {/* Data Display */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
        {/* Scénarios */}
        <div>
          <h3>Scenarios ({scenarios.length})</h3>
          <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
            {scenarios.map(scenario => (
              <div key={scenario.id} style={{
                padding: '10px',
                marginBottom: '5px',
                backgroundColor: scenario.isActive ? '#d4edda' : '#f8f9fa',
                border: '1px solid #ddd',
                borderRadius: '5px'
              }}>
                <strong>{scenario.name}</strong>
                <div>Vehicles: {scenario.vehicleCount}</div>
                <div>Density: {scenario.trafficDensity}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Simulation Status */}
        <div>
          <h3>Simulation Status</h3>
          {simulationStatus && (
            <div style={{
              padding: '15px',
              backgroundColor: simulationStatus.status === 'running' ? '#d4edda' : 
                               simulationStatus.status === 'paused' ? '#fff3cd' : '#f8d7da',
              border: '1px solid #ddd',
              borderRadius: '5px'
            }}>
              <div><strong>Status:</strong> {simulationStatus.status}</div>
              <div><strong>Scenario:</strong> {simulationStatus.currentScenario || 'None'}</div>
              <div><strong>Elapsed Time:</strong> {simulationStatus.elapsedTime?.toFixed(1)}s</div>
              <div><strong>Total Vehicles:</strong> {simulationStatus.totalVehicles}</div>
            </div>
          )}
        </div>

        {/* Metrics */}
        {metrics && (
          <div style={{ gridColumn: '1 / -1' }}>
            <h3>Current Metrics</h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '10px',
              padding: '15px',
              backgroundColor: '#e9ecef',
              border: '1px solid #ddd',
              borderRadius: '5px'
            }}>
              <div><strong>Total Vehicles:</strong> {metrics.totalVehicles}</div>
              <div><strong>Avg Speed:</strong> {metrics.avgSpeed} km/h</div>
              <div><strong>CO2 Emissions:</strong> {metrics.co2Emissions} g</div>
              <div><strong>Congestion:</strong> {metrics.congestionLevel}</div>
              <div><strong>Throughput:</strong> {metrics.throughput}</div>
              <div><strong>Emergency Vehicles:</strong> {metrics.emergencyVehiclesActive}</div>
            </div>
          </div>
        )}
      </div>

      {/* Log */}
      <div>
        <h3>Activity Log</h3>
        <div style={{
          height: '200px',
          overflowY: 'auto',
          backgroundColor: '#f8f9fa',
          border: '1px solid #ddd',
          borderRadius: '5px',
          padding: '10px',
          fontFamily: 'monospace',
          fontSize: '12px'
        }}>
          {log.map((entry, index) => (
            <div key={index} style={{ marginBottom: '5px' }}>{entry}</div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ConnectionTest;