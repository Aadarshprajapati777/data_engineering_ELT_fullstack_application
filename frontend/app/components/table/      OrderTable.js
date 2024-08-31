// app/components/table/OrderTable.js
import React from 'react';

const OrderTable = ({ orders }) => {
  return (
    <table className="min-w-full bg-white">
      <thead>
        <tr>
          <th className="py-2 px-4 border-b">Order ID</th>
          <th className="py-2 px-4 border-b">Net Amount</th>
          <th className="py-2 px-4 border-b">Invoice Amount</th>
          <th className="py-2 px-4 border-b">Order Date</th>
          <th className="py-2 px-4 border-b">Product Description</th>
        </tr>
      </thead>
      <tbody>
        {orders.map((order) => (
          <tr key={order.order_id}>
            <td className="py-2 px-4 border-b">{order.order_id}</td>
            <td className="py-2 px-4 border-b">{order.net_amount}</td>
            <td className="py-2 px-4 border-b">{order.invoice_amount}</td>
            <td className="py-2 px-4 border-b">{order.order_date}</td>
            <td className="py-2 px-4 border-b">{order.p_description}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default OrderTable;
