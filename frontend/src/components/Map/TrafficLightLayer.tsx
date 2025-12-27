import { CircleMarker, Popup } from 'react-leaflet';
import { useSimulationStore } from '../../stores';
import { TrafficLight } from '../../types';
import { TRAFFIC_LIGHT_COLORS } from '../../utils/constants';

export const TrafficLightLayer = () => {
  const { trafficLights } = useSimulationStore();

  const lightsArray = Array.from(trafficLights.values());

  return (
    <>
      {lightsArray.map((light) => (
        <TrafficLightMarker key={light.id} light={light} />
      ))}
    </>
  );
};

interface TrafficLightMarkerProps {
  light: TrafficLight;
}

const TrafficLightMarker = ({ light }: TrafficLightMarkerProps) => {
  const getMainColor = (state: string): string => {
    const firstChar = state[0];
    return TRAFFIC_LIGHT_COLORS[firstChar as keyof typeof TRAFFIC_LIGHT_COLORS] || '#94a3b8';
  };

  const color = getMainColor(light.state);

  return (
    <CircleMarker
      center={[light.position.lat, light.position.lng]}
      radius={5}
      pathOptions={{
        fillColor: color,
        fillOpacity: 0.9,
        color: '#1f2937',
        weight: 2,
      }}
    >
      <Popup>
        <div className="p-2">
          <div className="font-semibold text-sm mb-1">Traffic Light {light.id}</div>
          <div className="text-xs space-y-1">
            <div>State: {light.state}</div>
            <div>Phase: {light.currentPhase + 1}/{light.phases.length}</div>
            {light.remainingDuration && (
              <div>Remaining: {light.remainingDuration}s</div>
            )}
          </div>
        </div>
      </Popup>
    </CircleMarker>
  );
};
