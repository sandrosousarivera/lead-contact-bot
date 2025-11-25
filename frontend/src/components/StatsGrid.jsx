export default function StatsGrid({ stats }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
      <div className="stat-card">
        <div className="text-4xl font-bold mb-2">{stats.total}</div>
        <div className="text-gray-600 font-medium">Total Leads</div>
      </div>
      <div className="stat-card highlight">
        <div className="text-4xl font-bold mb-2">{stats.no_website}</div>
        <div className="font-medium">No Website</div>
      </div>
      <div className="stat-card">
        <div className="text-4xl font-bold mb-2">{stats.has_website}</div>
        <div className="text-gray-600 font-medium">Has Website</div>
      </div>
    </div>
  );
}
