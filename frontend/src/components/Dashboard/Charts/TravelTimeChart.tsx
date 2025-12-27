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
  ChartOptions,
} from 'chart.js';
import { Card } from '../../common';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export const TravelTimeChart = () => {
  const data = {
    labels: ['0s', '10s', '20s', '30s', '40s', '50s', '60s'],
    datasets: [
      {
        label: 'Travel Time (minutes)',
        data: [3.5, 3.2, 3.8, 3.6, 3.4, 3.7, 3.3],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
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
          text: 'Minutes',
        },
      },
    },
  };

  return (
    <Card title="Average Travel Time" padding="md">
      <div className="h-64 mt-4">
        <Line data={data} options={options} />
      </div>
    </Card>
  );
};
