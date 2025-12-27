import { Card, Badge } from '../common';
import { useMetrics } from '../../hooks/useMetrics';
import { Car, Wind, Clock, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react';

export const MetricsPanel = () => {
  const { formattedMetrics, performanceStatus } = useMetrics();

  const statusColors = {
    excellent: 'success',
    good: 'success',
    moderate: 'warning',
    poor: 'error',
    unknown: 'neutral',
  } as const;

  const statusLabels = {
    excellent: 'Excellent',
    good: 'Good',
    moderate: 'Moderate',
    poor: 'Poor',
    unknown: 'Unknown',
  };

  const metrics = [
    {
      label: 'Total Vehicles',
      value: formattedMetrics.totalVehicles,
      icon: Car,
      color: 'text-blue-600',
    },
    {
      label: 'Avg Speed',
      value: formattedMetrics.avgSpeed,
      icon: TrendingUp,
      color: 'text-green-600',
    },
    {
      label: 'Avg Travel Time',
      value: formattedMetrics.avgTravelTime,
      icon: Clock,
      color: 'text-orange-600',
    },
    {
      label: 'CO₂ Emissions',
      value: formattedMetrics.co2Emissions,
      icon: Wind,
      color: 'text-purple-600',
    },
    {
      label: 'Emergency Vehicles',
      value: formattedMetrics.emergencyVehiclesActive,
      icon: AlertTriangle,
      color: 'text-red-600',
    },
    {
      label: 'Completed Trips',
      value: formattedMetrics.completedTrips,
      icon: CheckCircle,
      color: 'text-teal-600',
    },
  ];

  return (
    <div className="space-y-4">
      <Card padding="md">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Performance Status</h3>
          <Badge variant={statusColors[performanceStatus]}>
            {statusLabels[performanceStatus]}
          </Badge>
        </div>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <Card key={metric.label} padding="md">
              <div className="flex items-start space-x-3">
                <div className={`p-2 rounded-lg bg-gray-100 ${metric.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <p className="text-sm text-gray-600">{metric.label}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{metric.value}</p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      <Card padding="md" title="Vehicle Distribution">
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div>
            <p className="text-sm text-gray-600">Passenger</p>
            <p className="text-lg font-semibold text-gray-900">
              {formattedMetrics.vehiclesByType.passenger}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Bus</p>
            <p className="text-lg font-semibold text-gray-900">
              {formattedMetrics.vehiclesByType.bus}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Truck</p>
            <p className="text-lg font-semibold text-gray-900">
              {formattedMetrics.vehiclesByType.truck}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Emergency</p>
            <p className="text-lg font-semibold text-red-600">
              {formattedMetrics.vehiclesByType.emergency}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};
