// app/summary/page.js
"use client"
import React, { useEffect, useState } from 'react';
import Sidebar from '../components/layout/      Sidebar';
import Topbar from '../components/layout/      Topbar';
import OrderTable from '../components/table/      OrderTable';
import { fetchGroupedData } from '../api/api'

const SummaryPage = () => {
  const [groupedData, setGroupedData] = useState([]);

  useEffect(() => {
    const loadGroupedData = async () => {
      const data = await fetchGroupedData();
      setGroupedData(data);
    };
    loadGroupedData();
  }, []);

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Topbar />
        <div className="p-4">
          <OrderTable orders={groupedData} />
        </div>
      </div>
    </div>
  );
};

export default SummaryPage;
