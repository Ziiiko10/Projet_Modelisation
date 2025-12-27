import { Layers } from 'lucide-react';
import { useUIStore } from '../../stores';
import { Card, Button } from '../common';
import { clsx } from 'clsx';

export const MapControls = () => {
  const { activeLayer, setActiveLayer } = useUIStore();

  const layers = [
    { id: 'all', label: 'All Layers' },
    { id: 'vehicles', label: 'Vehicles Only' },
    { id: 'traffic-lights', label: 'Traffic Lights Only' },
    { id: 'roads', label: 'Roads Only' },
  ] as const;

  return (
    <div className="absolute top-4 right-4 z-[1000]">
      <Card padding="sm" className="w-48">
        <div className="flex items-center space-x-2 mb-3">
          <Layers className="w-4 h-4 text-gray-700" />
          <h3 className="text-sm font-semibold text-gray-900">Map Layers</h3>
        </div>
        <div className="space-y-1">
          {layers.map((layer) => (
            <button
              key={layer.id}
              onClick={() => setActiveLayer(layer.id as typeof activeLayer)}
              className={clsx(
                'w-full text-left px-3 py-2 rounded text-sm transition-colors',
                activeLayer === layer.id
                  ? 'bg-primary-100 text-primary-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-100'
              )}
            >
              {layer.label}
            </button>
          ))}
        </div>
      </Card>
    </div>
  );
};
