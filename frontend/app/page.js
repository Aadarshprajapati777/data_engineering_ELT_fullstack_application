// app/page.js (or similar)
"use client"
import React, { useEffect, useState } from 'react';
import Sidebar from './components/layout/      Sidebar';
import Topbar from './components/layout/      Topbar';
import DashboardCard from './components/dashboard/      DashboardCard';
import { BarChart, PieChart } from './components/dashboard/      Chart';
import { fetchSummary } from './api/api';

const HomePage = () => {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    const loadSummary = async () => {
      const data = await fetchSummary();
      // Ensure the data structure is correct here
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
          <DashboardCard title="Previous Month Order" value={summary?.prevMonthOrder || 0} />
          <DashboardCard title="Order & Payment Received" value={summary?.orderPaymentReceived || 0} />
          <DashboardCard title="Payment Pending" value={summary?.paymentPending || 0} />
          {/* Add more cards as necessary */}
        </div>
        <div className="p-4 grid grid-cols-2 gap-4">
          <BarChart data={summary?.barChartData || { labels: [], datasets: [] }} />
          <PieChart data={summary?.pieChartData || { labels: [], datasets: [] }} />
        </div>
      </div>
    </div>
  );
};

export default HomePage;
