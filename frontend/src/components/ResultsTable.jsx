export default function ResultsTable({ leads, onDelete }) {
  if (leads.length === 0) {
    return (
      <div className="card text-center py-16">
        <p className="text-gray-500 text-lg italic">
          No leads found. Try adjusting your filters or start a new search.
        </p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">📊 Results</h2>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100 border-b-2 border-gray-300">
              <th className="px-6 py-4 text-left font-semibold text-gray-800">
                Business Name
              </th>
              <th className="px-6 py-4 text-left font-semibold text-gray-800">
                Category
              </th>
              <th className="px-6 py-4 text-left font-semibold text-gray-800">
                Phone
              </th>
              <th className="px-6 py-4 text-left font-semibold text-gray-800">
                Address
              </th>
              <th className="px-6 py-4 text-left font-semibold text-gray-800">
                Website
              </th>
              <th className="px-6 py-4 text-left font-semibold text-gray-800">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {leads.map((lead) => (
              <tr
                key={lead.id}
                className="border-b border-gray-200 hover:bg-gray-50"
              >
                <td className="px-6 py-4 font-medium text-gray-900">
                  {lead.name}
                </td>
                <td className="px-6 py-4 text-gray-700">{lead.category}</td>
                <td className="px-6 py-4 text-gray-700">{lead.phone}</td>
                <td className="px-6 py-4 text-gray-700 text-sm">
                  {lead.address}
                </td>
                <td className="px-6 py-4">
                  {lead.has_website ? (
                    <a
                      href={lead.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-purple-600 hover:text-purple-800 font-medium"
                    >
                      Visit
                    </a>
                  ) : (
                    <span className="inline-block bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-semibold">
                      No Website
                    </span>
                  )}
                </td>
                <td className="px-6 py-4">
                  <button
                    onClick={() => onDelete(lead.id)}
                    className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm font-medium"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
