import React, { useState } from 'react'

export default function SearchForm({ onSubmit, isLoading, progress, message }) {
  const [niche, setNiche] = useState('')
  const [location, setLocation] = useState('España')
  const [maxPages, setMaxPages] = useState(3)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!niche.trim()) {
      alert('Please enter a niche')
      return
    }
    onSubmit({ niche, location, max_pages: maxPages })
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">🔍 Start New Search</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Business Niche/Category
          </label>
          <input
            type="text"
            value={niche}
            onChange={(e) => setNiche(e.target.value)}
            placeholder="e.g., restaurantes, fontaneros, talleres"
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-purple-500"
            disabled={isLoading}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Location
            </label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-purple-500"
              disabled={isLoading}
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Pages to Scrape
            </label>
            <input
              type="number"
              value={maxPages}
              onChange={(e) => setMaxPages(Math.min(10, Math.max(1, parseInt(e.target.value) || 1)))}
              min="1"
              max="10"
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-purple-500"
              disabled={isLoading}
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className={`btn btn-primary w-full ${isLoading ? 'opacity-60 cursor-not-allowed' : ''}`}
        >
          {isLoading ? '⏳ Scraping...' : '🚀 Start Scraping'}
        </button>
      </form>

      {isLoading && (
        <div className="mt-6">
          <div className="w-full h-8 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-purple-600 to-pink-600 transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <p className="text-center text-gray-600 text-sm mt-3">{message}</p>
        </div>
      )}
    </div>
  )
}
