"use client"
import React, { useEffect, useState } from 'react';
import Sidebar from '../components/layout/      Sidebar';
import Topbar from '../components/layout/      Topbar';
import SummaryTable from '../components/table/SummaryTable';
import Loader from '../components/loader/Loader';
import { fetchSummary } from '../api/api';
import { AnimatePresence } from 'framer-motion';

const SummaryPage = () => {
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(true);  

  useEffect(() => {
    const loadSummary = async () => {
      try {
        const data = await fetchSummary();
        setSummary(data);  
      } catch (error) {
        console.error('Error fetching summary data:', error);
      } finally {
        setLoading(false);  
      }
    };
    loadSummary();
  }, []);

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Topbar />
        <div className="p-4">
          <AnimatePresence>
            {loading && <Loader />}
          </AnimatePresence>

          <AnimatePresence>
            {!loading && <SummaryTable summary={summary} />}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default SummaryPage;
