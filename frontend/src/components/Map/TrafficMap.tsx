import { MapContainer, TileLayer } from 'react-leaflet';
import { useUIStore } from '../../stores';
import { VehicleLayer } from './VehicleLayer';
import { TrafficLightLayer } from './TrafficLightLayer';
import { MapControls } from './MapControls';
import { DEFAULT_MAP_CENTER, DEFAULT_MAP_ZOOM } from '../../utils/constants';

export const TrafficMap = () => {
  const { activeLayer } = useUIStore();

  const showVehicles = activeLayer === 'all' || activeLayer === 'vehicles';
  const showTrafficLights = activeLayer === 'all' || activeLayer === 'traffic-lights';

  return (
    <div className="relative w-full h-full">
      <MapContainer
        center={[DEFAULT_MAP_CENTER.lat, DEFAULT_MAP_CENTER.lng]}
        zoom={DEFAULT_MAP_ZOOM}
        className="w-full h-full"
        zoomControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {showVehicles && <VehicleLayer />}
        {showTrafficLights && <TrafficLightLayer />}
      </MapContainer>

      <MapControls />
    </div>
  );
};
