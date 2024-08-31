// app/components/layout/Topbar.js
const Topbar = () => {
    return (
      <div className="bg-white shadow-md p-4 flex justify-between items-center">
        <div className="text-purple-700 text-lg font-bold">Dashboard</div>
        <input type="text" placeholder="Search..." className="border px-2 py-1 rounded-md" />
      </div>
    );
  };
  
  export default Topbar;
  