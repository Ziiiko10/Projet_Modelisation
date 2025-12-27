import { useEffect, useRef } from 'react';
import { TrafficMap } from '../components/Map/TrafficMap';
import { MetricsPanel } from '../components/Dashboard/MetricsPanel';
import { ControlPanel } from '../components/Dashboard/ControlPanel';
import { TravelTimeChart } from '../components/Dashboard/Charts/TravelTimeChart';
import { EmissionsChart } from '../components/Dashboard/Charts/EmissionsChart';
import { useWebSocket } from '../hooks/useWebSocket';
import { useUIStore } from '../stores/ui.store';

export const Dashboard = () => {
  const { isConnected } = useWebSocket(); // Ne pas appeler connect ici!
  const { mapFullscreen } = useUIStore();
  const initializedRef = useRef(false);

  // Évitez tout useEffect qui pourrait causer des re-rendus
  useEffect(() => {
    if (!initializedRef.current) {
      console.log('Dashboard mounted');
      initializedRef.current = true;
    }
  }, []);

  if (mapFullscreen) {
    return (
      <div className="h-screen w-screen">
        <TrafficMap />
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col md:flex-row">
      <div className="flex-1">
        <TrafficMap />
      </div>
      <div className="w-full md:w-96 border-l">
        <div className="p-4 space-y-6">
          <div className="mb-4">
            <div className={`inline-block px-3 py-1 rounded-full text-sm ${isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
              {isConnected ? 'Connected' : 'Disconnected'}
            </div>
          </div>
          <ControlPanel />
          <MetricsPanel />
          <TravelTimeChart />
          <EmissionsChart />
        </div>
      </div>
    </div>
  );
};