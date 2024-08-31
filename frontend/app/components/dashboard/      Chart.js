import { Bar, Pie } from 'react-chartjs-2';
import 'chart.js/auto';

export const BarChart = ({ data }) => {
  if (!data || !data.labels || !data.datasets) {
    return <p>Loading...</p>; 
  }

  return <Bar data={data} options={{ responsive: true, maintainAspectRatio: false }} />;
};

export const PieChart = ({ data }) => {
  if (!data || !data.labels || !data.datasets) {
    return <p>Loading...</p>; 
  }

  return <Pie data={data} options={{ responsive: true, maintainAspectRatio: false }} />;
};
