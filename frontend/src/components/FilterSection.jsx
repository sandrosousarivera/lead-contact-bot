export default function FilterSection({ filterType, setFilterType, searchTerm, setSearchTerm, onExport, onClearAll }) {
  return (
    <div className="flex flex-col md:flex-row gap-4 mb-6 items-center">
      <div className="flex-1">
        <label className="block text-sm font-semibold text-white mb-2">Filter:</label>
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="w-full px-4 py-2 border-2 border-white rounded-lg focus:outline-none bg-white"
        >
          <option value="all">All Leads</option>
          <option value="no_website">No Website Only</option>
          <option value="has_website">Has Website</option>
        </select>
      </div>

      <div className="flex-1">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search by name or category..."
          className="w-full px-4 py-2 border-2 border-white rounded-lg focus:outline-none"
        />
      </div>

      <div className="flex gap-2">
        <button
          onClick={onExport}
          className="btn bg-green-500 text-white hover:bg-green-600"
        >
          📥 Export
        </button>
        <button
          onClick={onClearAll}
          className="btn btn-danger"
        >
          🗑️ Clear
        </button>
      </div>
    </div>
  )
}
