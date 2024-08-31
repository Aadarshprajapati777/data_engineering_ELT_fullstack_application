// app/dashboard/page.js
import React, { useEffect, useState } from 'react';
import Sidebar from '../components/layout/Sidebar';
import Topbar from '../components/layout/Topbar';
import DashboardCard from '../components/dashboard/DashboardCard';
import { BarChart, PieChart } from '../components/dashboard/Chart';
import { fetchSummary } from '../api/api';

const Dashboard = () => {
  const [summary, setSummary] = useState({});

  useEffect(() => {
    const loadSummary = async () => {
      const data = await fetchSummary();
      setSummary(data);
    };
    loadSummary();
  }, []);

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Topbar />
        <div className="p-4 grid grid-cols-3 gap-4">
          <DashboardCard title="Previous Month Order" value={summary.prevMonthOrder} />
          <DashboardCard title="Order & Payment Received" value={summary.orderPaymentReceived} />
          <DashboardCard title="Payment Pending" value={summary.paymentPending} />
          {/* Add more cards as necessary */}
        </div>
        <div className="p-4 grid grid-cols-2 gap-4">
          <BarChart data={summary.barChartData} />
          <PieChart data={summary.pieChartData} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
