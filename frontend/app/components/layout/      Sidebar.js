import Link from 'next/link';

const Sidebar = () => {
  return (
    <div className="h-screen w-20 bg-gray-800 text-white flex flex-col items-center py-4">
      <Link href="/" className="mb-6">🏠</Link>
      <Link href="/upload" className="mb-6">⬆️</Link>
      <Link href="/summary" className="mb-6">📊</Link>
      <Link href="/orders">📄</Link>
    </div>
  );
};

export default Sidebar;
