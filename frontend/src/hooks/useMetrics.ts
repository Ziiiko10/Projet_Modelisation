import { useMemo } from 'react';
import { useSimulationStore } from '../stores';

export const useMetrics = () => {
  const { metrics, vehicles } = useSimulationStore();

  const formattedMetrics = useMemo(() => {
    if (!metrics) {
      return {
        totalVehicles: 0,
        avgSpeed: '0 km/h',
        avgTravelTime: '0 min',
        co2Emissions: '0 kg/h',
        emergencyVehiclesActive: 0,
        completedTrips: 0,
        waitingTime: '0 s',
        vehiclesByType: {
          passenger: 0,
          bus: 0,
          truck: 0,
          emergency: 0,
        },
      };
    }

    const vehiclesByType = {
      passenger: 0,
      bus: 0,
      truck: 0,
      emergency: 0,
    };

    Array.from(vehicles.values()).forEach((vehicle) => {
      vehiclesByType[vehicle.type]++;
    });

    return {
      totalVehicles: metrics.totalVehicles,
      avgSpeed: `${metrics.avgSpeed.toFixed(1)} km/h`,
      avgTravelTime: `${(metrics.avgTravelTime / 60).toFixed(1)} min`,
      co2Emissions: `${metrics.co2Emissions.toFixed(1)} kg/h`,
      emergencyVehiclesActive: metrics.emergencyVehiclesActive,
      completedTrips: metrics.completedTrips,
      waitingTime: `${metrics.waitingTime.toFixed(0)} s`,
      vehiclesByType,
    };
  }, [metrics, vehicles]);

  const performanceStatus = useMemo(() => {
    if (!metrics) return 'unknown';

    if (metrics.avgSpeed > 40 && metrics.avgTravelTime < 180) {
      return 'excellent';
    } else if (metrics.avgSpeed > 25 && metrics.avgTravelTime < 300) {
      return 'good';
    } else if (metrics.avgSpeed > 15 && metrics.avgTravelTime < 420) {
      return 'moderate';
    } else {
      return 'poor';
    }
  }, [metrics]);

  return {
    metrics,
    formattedMetrics,
    performanceStatus,
  };
};
