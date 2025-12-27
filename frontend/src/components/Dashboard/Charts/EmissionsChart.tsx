import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ChartOptions,
} from 'chart.js';
import { Card } from '../../common';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export const EmissionsChart = () => {
  const data = {
    labels: ['0s', '10s', '20s', '30s', '40s', '50s', '60s'],
    datasets: [
      {
        label: 'CO₂ Emissions (kg/h)',
        data: [45, 48, 52, 50, 47, 49, 46],
        borderColor: 'rgb(139, 92, 246)',
        backgroundColor: 'rgba(139, 92, 246, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'kg/h',
        },
      },
    },
  };

  return (
    <Card title="CO₂ Emissions" padding="md">
      <div className="h-64 mt-4">
        <Line data={data} options={options} />
      </div>
    </Card>
  );
};
