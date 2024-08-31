import React from 'react';

const OrderTable = ({ orders }) => {
  console.log("orders: ", orders);
  
  if (!orders || orders.length === 0) {
    return <p>No orders available.</p>;
  }

  return (
    <table className="min-w-full bg-white">
      <thead>
        <tr>
          <th className="py-2 px-4 border-b">Order ID</th>
          <th className="py-2 px-4 border-b">Net Amount</th>
          <th className="py-2 px-4 border-b">Invoice Amount</th>
          <th className="py-2 px-4 border-b">Classification</th>
        </tr>
      </thead>
      <tbody>
        {orders.map((order) => {
          const transactionType = Object.keys(order.transactions)[0]; 
          const transaction = order.transactions[transactionType];
          
          return (
            <tr key={order.order_id}>
              <td className="py-2 px-4 border-b">{order.order_id}</td>
              <td className="py-2 px-4 border-b">{transaction.net_amount}</td>
              <td className="py-2 px-4 border-b">{transaction.invoice_amount}</td>
              <td className="py-2 px-4 border-b">{transaction.classification}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default OrderTable;
