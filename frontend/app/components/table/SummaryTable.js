import React from 'react';

const SummaryTable = ({ summary }) => {
    console.log("summary: ", summary)
    if (!Array.isArray(summary) || summary.length === 0) {
      return <p>No data available.</p>;
    }
  
    return (
      <div className="bg-orange-100 p-6 rounded-lg shadow-lg">
        <h2 className="text-lg font-bold mb-4 text-blue-900">Blank Transaction Summary</h2>
        <table className="min-w-full text-left border-collapse">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b bg-orange-500 text-white">P_Description</th>
              <th className="py-2 px-4 border-b bg-orange-500 text-white">SUM of Net Amount</th>
            </tr>
          </thead>
          <tbody>
            {summary.map((item, index) => (
              <tr key={index} className="hover:bg-orange-200">
                <td className="py-2 px-4 border-b">{item.p_description}</td>
                <td className="py-2 px-4 border-b text-right">{item["Sum of Net Amount"].toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };
  
  export default SummaryTable;