import { Card } from '../components/common';
import { TravelTimeChart, EmissionsChart } from '../components/Dashboard';
import { useMetrics } from '../hooks/useMetrics';
import { BarChart3, TrendingDown, TrendingUp } from 'lucide-react';

export const Analysis = () => {
  const { formattedMetrics, performanceStatus } = useMetrics();

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Analysis</h1>
        <p className="text-gray-600 mt-2">Performance metrics and historical data</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <Card padding="md">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-gray-600">Performance Status</p>
              <p className="text-2xl font-bold text-gray-900 mt-1 capitalize">
                {performanceStatus}
              </p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <BarChart3 className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </Card>

        <Card padding="md">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-gray-600">Average Speed</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {formattedMetrics.avgSpeed}
              </p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </Card>

        <Card padding="md">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-gray-600">CO₂ Emissions</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {formattedMetrics.co2Emissions}
              </p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <TrendingDown className="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TravelTimeChart />
        <EmissionsChart />
      </div>

      <div className="mt-6">
        <Card padding="md" title="Historical Comparisons">
          <div className="mt-4 text-center py-12">
            <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No historical data available yet</p>
            <p className="text-sm text-gray-500 mt-2">
              Run simulations to generate comparative analytics
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};
