"use client"
import React from 'react';

import PaginatedOrderTable from '../components/table/PaginatedOrderTable';

const OrdersPage = () => {
  return (
    <div className="flex">
      <div className="flex-1 flex flex-col">
        <PaginatedOrderTable />
      </div>
    </div>
  );
};

export default OrdersPage;
