// app/components/dashboard/Chart.js
import { Bar, Pie } from 'react-chartjs-2';
import 'chart.js/auto';

export const BarChart = ({ data }) => {
  if (!data || !data.labels || !data.datasets) {
    return <p>Loading...</p>; // or handle it in some other way
  }

  return <Bar data={data} options={{ responsive: true, maintainAspectRatio: false }} />;
};

export const PieChart = ({ data }) => {
  if (!data || !data.labels || !data.datasets) {
    return <p>Loading...</p>; // or handle it in some other way
  }

  return <Pie data={data} options={{ responsive: true, maintainAspectRatio: false }} />;
};
