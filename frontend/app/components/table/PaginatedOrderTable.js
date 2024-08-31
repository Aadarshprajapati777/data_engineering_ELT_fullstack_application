"use client"
import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/layout/      Sidebar';
import Topbar from '../../components/layout/      Topbar';
import { fetchGroupedData } from '../../api/api';
import { motion } from 'framer-motion';           

const PaginatedOrderTable = () => {
  const [orders, setOrders] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const loadMoreOrders = async () => {
    if (loading || !hasMore) return;
    setLoading(true);

    try {
      const response = await fetchGroupedData(page);
      if (response.grouped_data.length > 0) {
        setOrders(prevOrders => [...prevOrders, ...response.grouped_data]);
        setPage(prevPage => prevPage + 1);
      } else {
        setHasMore(false);
      }
    } catch (error) {
      console.error("Error fetching orders:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMoreOrders();
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + document.documentElement.scrollTop >=
        document.documentElement.offsetHeight - 100 &&
        hasMore &&
        !loading
      ) {
        loadMoreOrders();
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [loading, hasMore]);

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Fixed Sidebar */}
      <div className="flex-none">
        <Sidebar />
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-y-auto">
        <Topbar />

        <div className="p-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <table className="min-w-full bg-white rounded-lg shadow-lg">
              <thead>
                <tr className="bg-purple-600 text-white">
                  <th className="py-2 px-4 border-b">Order ID</th>
                  <th className="py-2 px-4 border-b">Transaction Type</th>
                  <th className="py-2 px-4 border-b">Net Amount</th>
                  <th className="py-2 px-4 border-b">Invoice Amount</th>
                  <th className="py-2 px-4 border-b">Classification</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order, index) =>
                  Object.keys(order.transactions).map((transactionType, subIndex) => {
                    const transaction = order.transactions[transactionType];
                    return (
                      <tr key={`${index}-${subIndex}`} className="hover:bg-gray-200">
                        <td className="py-2 px-4 border-b">{order.order_id}</td>
                        <td className="py-2 px-4 border-b">{transactionType}</td>
                        <td className="py-2 px-4 border-b text-right">
                          {transaction.net_amount !== undefined
                            ? transaction.net_amount.toLocaleString()
                            : 'N/A'}
                        </td>
                        <td className="py-2 px-4 border-b text-right">
                          {transaction.invoice_amount !== undefined
                            ? transaction.invoice_amount.toLocaleString()
                            : 'N/A'}
                        </td>
                        <td className="py-2 px-4 border-b">{transaction.classification || 'N/A'}</td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </motion.div>

          {loading && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="text-center py-4 text-gray-500"
            >
              Loading more orders...
            </motion.p>
          )}
          {!hasMore && !loading && (
            <p className="text-center py-4 text-gray-500">No more orders to load.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default PaginatedOrderTable;
