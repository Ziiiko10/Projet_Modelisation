import { useEffect } from 'react';
import { CircleMarker, Popup, useMap } from 'react-leaflet';
import { useSimulationStore } from '../../stores';
import { VEHICLE_COLORS } from '../../utils/constants';
import { Vehicle } from '../../types';

export const VehicleLayer = () => {
  const map = useMap();
  const { vehicles } = useSimulationStore();

  const vehicleArray = Array.from(vehicles.values());

  return (
    <>
      {vehicleArray.map((vehicle) => (
        <VehicleMarker key={vehicle.id} vehicle={vehicle} />
      ))}
    </>
  );
};

interface VehicleMarkerProps {
  vehicle: Vehicle;
}

const VehicleMarker = ({ vehicle }: VehicleMarkerProps) => {
  const color = vehicle.color || VEHICLE_COLORS[vehicle.type];

  return (
    <CircleMarker
      center={[vehicle.position.lat, vehicle.position.lng]}
      radius={vehicle.type === 'emergency' ? 8 : 6}
      pathOptions={{
        fillColor: color,
        fillOpacity: 0.8,
        color: vehicle.type === 'emergency' ? '#fff' : color,
        weight: vehicle.type === 'emergency' ? 2 : 1,
      }}
    >
      <Popup>
        <div className="p-2">
          <div className="font-semibold text-sm mb-1">Vehicle {vehicle.id}</div>
          <div className="text-xs space-y-1">
            <div>Type: {vehicle.type}</div>
            <div>Speed: {vehicle.speed.toFixed(1)} km/h</div>
            <div>Lane: {vehicle.lane}</div>
          </div>
        </div>
      </Popup>
    </CircleMarker>
  );
};
