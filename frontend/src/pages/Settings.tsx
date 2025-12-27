import { Card, Button } from '../components/common';
import { Settings as SettingsIcon, Map, PieChart, Info } from 'lucide-react';

export const Settings = () => {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-2">Configure your Urban Flow experience</p>
      </div>

      <div className="space-y-6">
        <Card padding="md" title="Map Preferences">
          <div className="mt-4 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Default Map Center</label>
                <p className="text-xs text-gray-500">Paris, France</p>
              </div>
              <Button variant="secondary" size="sm">Change</Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Default Zoom Level</label>
                <p className="text-xs text-gray-500">13</p>
              </div>
              <Button variant="secondary" size="sm">Change</Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Show Vehicle Labels</label>
                <p className="text-xs text-gray-500">Display vehicle IDs on map</p>
              </div>
              <button
                className="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-300"
              >
                <span className="inline-block h-4 w-4 transform rounded-full bg-white translate-x-1" />
              </button>
            </div>
          </div>
        </Card>

        <Card padding="md" title="Simulation Preferences">
          <div className="mt-4 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Auto-pause on Emergency</label>
                <p className="text-xs text-gray-500">Pause when emergency vehicle is detected</p>
              </div>
              <button
                className="relative inline-flex h-6 w-11 items-center rounded-full bg-green-600"
              >
                <span className="inline-block h-4 w-4 transform rounded-full bg-white translate-x-6" />
              </button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-700">Real-time Metrics</label>
                <p className="text-xs text-gray-500">Update metrics every second</p>
              </div>
              <button
                className="relative inline-flex h-6 w-11 items-center rounded-full bg-green-600"
              >
                <span className="inline-block h-4 w-4 transform rounded-full bg-white translate-x-6" />
              </button>
            </div>
          </div>
        </Card>

        <Card padding="md" title="About">
          <div className="mt-4 space-y-3 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <Info className="w-4 h-4" />
              <span>Urban Flow v1.0.0</span>
            </div>
            <p>Traffic Management Digital Twin System</p>
            <p className="text-xs text-gray-500">
              Built with React, TypeScript, Leaflet, and SUMO integration
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};
