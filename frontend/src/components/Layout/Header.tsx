import { Menu, Maximize2, Minimize2 } from 'lucide-react';
import { useUIStore } from '../../stores';
import { Button } from '../common';

export const Header = () => {
  const { toggleSidebar, mapFullscreen, toggleMapFullscreen } = useUIStore();

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="sm" onClick={toggleSidebar}>
            <Menu className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Urban Flow</h1>
            <p className="text-sm text-gray-500">Traffic Management Digital Twin</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <Button variant="ghost" size="sm" onClick={toggleMapFullscreen}>
            {mapFullscreen ? (
              <Minimize2 className="w-5 h-5" />
            ) : (
              <Maximize2 className="w-5 h-5" />
            )}
          </Button>
        </div>
      </div>
    </header>
  );
};
