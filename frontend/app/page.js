"use client";
import React, { useEffect, useState, useMemo, useCallback } from 'react';
import dynamic from 'next/dynamic';
import CHART_COLORS from './components/dashboard/ChartColor';

// Lazy load components that are not immediately necessary
const Sidebar = dynamic(() => import('./components/layout/      Sidebar'), { ssr: false });
const Topbar = dynamic(() => import('./components/layout/      Topbar'), { ssr: false });
const DashboardCard = dynamic(() => import('./components/dashboard/      DashboardCard'), { ssr: false });
const BarChart = dynamic(() => import('./components/dashboard/      Chart').then(mod => mod.BarChart), { ssr: false });
const PieChart = dynamic(() => import('./components/dashboard/      Chart').then(mod => mod.PieChart), { ssr: false });
const Loader = dynamic(() => import('./components/loader/Loader'), { ssr: false }); 

import { fetchGroupedData } from './api/api';

const HomePage = () => {
  const [groupedData, setGroupedData] = useState([]);
  const [summary, setSummary] = useState({
    totalOrders: 0,
    orderPaymentReceived: 0,
    paymentPending: 0,
  });
  const [loading, setLoading] = useState(true); 
  

  useEffect(() => {
    loadGroupedData();
  }, []);

  const loadGroupedData = useCallback(async () => {
    try {
      const data = await fetchGroupedData();
      if (data && data.grouped_data) {
        setGroupedData(data.grouped_data);
        processSummary(data.grouped_data);
      }
    } catch (error) {
      console.error("Failed to load grouped data:", error);
    } finally {
      setLoading(false);
      
    }
  }, []);

  const processSummary = useCallback((data) => {
    const totalOrders = data.length;
    let orderPaymentReceived = 0;
    let paymentPending = 0;

    const classificationCounts = {};

    data.forEach((order) => {
      const transactionType = Object.keys(order.transactions)[0];
      const classification = order.transactions[transactionType]?.classification;

      if (classification === "Order & Payment Received") {
        orderPaymentReceived += 1;
      } else if (classification === "Payment Pending") {
        paymentPending += 1;
      }

      classificationCounts[classification] = (classificationCounts[classification] || 0) + 1;
    });

    setSummary({
      totalOrders,
      orderPaymentReceived,
      paymentPending,
      classificationCounts,
    });
  }, []);

  const barChartData = useMemo(() => ({
    labels: Object.keys(summary.classificationCounts || {}),
    datasets: [
      {
        label: 'Order Classifications',
        data: Object.values(summary.classificationCounts || {}),
        backgroundColor: CHART_COLORS.bar.backgroundColor,
        borderColor: CHART_COLORS.bar.borderColor,
        borderWidth: 1,
      },
    ],
  }), [summary.classificationCounts]);

  const pieChartData = useMemo(() => ({
    labels: Object.keys(summary.classificationCounts || {}),
    datasets: [
      {
        label: 'Order Classifications',
        data: Object.values(summary.classificationCounts || {}),
        backgroundColor: CHART_COLORS.pie,
        borderColor: CHART_COLORS.borderColor,
        borderWidth: 1,
      },
    ],
  }), [summary.classificationCounts]);

  return (
    <div className="flex h-screen bg-gray-100">
      <React.Suspense fallback={<div>Loading Sidebar...</div>}>
        <Sidebar />
      </React.Suspense>
      <div className="flex-1 flex flex-col">
        <React.Suspense fallback={<div>Loading Topbar...</div>}>
          <Topbar />
        </React.Suspense>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
            <DashboardCard title="Total Orders" value={summary.totalOrders} />
            <DashboardCard title="Order & Payment Received" value={summary.orderPaymentReceived} />
            <DashboardCard title="Payment Pending" value={summary.paymentPending} />
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-lg">
              {loading ? <Loader /> : <BarChart data={barChartData} />}
            </div>
            <div className="bg-white p-6 rounded-lg shadow-lg">
              {loading ? <Loader /> : <PieChart data={pieChartData} />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;