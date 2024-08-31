// app/components/dashboard/DashboardCard.js
const DashboardCard = ({ title, value }) => {
    return (
      <div className="bg-white p-4 rounded-md shadow-md w-full">
        <div className="text-gray-500">{title}</div>
        <div className="text-2xl font-bold">{value}</div>
      </div>
    );
  };
  
  export default DashboardCard;
  