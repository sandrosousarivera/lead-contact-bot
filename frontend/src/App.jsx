import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Header from './components/Header'
import StatsGrid from './components/StatsGrid'
import SearchForm from './components/SearchForm'
import FilterSection from './components/FilterSection'
import ResultsTable from './components/ResultsTable'

function App() {
  const [stats, setStats] = useState({ total: 0, no_website: 0, has_website: 0 })
  const [leads, setLeads] = useState([])
  const [scraping, setScraping] = useState(false)
  const [progress, setProgress] = useState(0)
  const [progressMessage, setProgressMessage] = useState('')
  const [filterType, setFilterType] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  const loadStats = async () => {
    try {
      const response = await axios.get('/api/stats')
      setStats(response.data)
    } catch (error) {
      console.error('Error loading stats:', error)
    }
  }

  const loadLeads = async () => {
    try {
      const response = await axios.get(`/api/leads?filter=${filterType}&search=${encodeURIComponent(searchTerm)}`)
      setLeads(response.data)
    } catch (error) {
      console.error('Error loading leads:', error)
    }
  }

  useEffect(() => {
    loadStats()
    loadLeads()
  }, [])

  useEffect(() => {
    loadLeads()
  }, [filterType, searchTerm])

  const startScraping = async (data) => {
    setScraping(true)
    setProgress(0)
    setProgressMessage('Initializing...')

    try {
      await axios.post('/api/start-scraping', data)

      // Poll for status
      const statusInterval = setInterval(async () => {
        try {
          const response = await axios.get('/api/status')
          setProgress(response.data.progress)
          setProgressMessage(response.data.message)

          if (!response.data.is_running) {
            clearInterval(statusInterval)
            setScraping(false)
            await loadStats()
            await loadLeads()
          }
        } catch (error) {
          console.error('Error checking status:', error)
        }
      }, 1000)
    } catch (error) {
      console.error('Error starting scraper:', error)
      setScraping(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this lead?')) return

    try {
      await axios.delete(`/api/delete-lead/${id}`)
      await loadStats()
      await loadLeads()
    } catch (error) {
      console.error('Error deleting lead:', error)
    }
  }

  const handleExport = async () => {
    try {
      const response = await axios.get('/api/export', { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `leads_${new Date().getTime()}.json`)
      document.body.appendChild(link)
      link.click()
      link.parentElement.removeChild(link)
    } catch (error) {
      console.error('Error exporting leads:', error)
    }
  }

  const handleClearAll = async () => {
    if (!confirm('Are you sure you want to delete ALL leads? This cannot be undone!')) return

    try {
      await axios.post('/api/clear-all')
      await loadStats()
      await loadLeads()
    } catch (error) {
      console.error('Error clearing leads:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-500 via-purple-400 to-pink-500 p-6">
      <div className="max-w-6xl mx-auto">
        <Header />
        <StatsGrid stats={stats} />
        <SearchForm onSubmit={startScraping} isLoading={scraping} progress={progress} message={progressMessage} />
        <FilterSection filterType={filterType} setFilterType={setFilterType} searchTerm={searchTerm} setSearchTerm={setSearchTerm} onExport={handleExport} onClearAll={handleClearAll} />
        <ResultsTable leads={leads} onDelete={handleDelete} />
      </div>
    </div>
  )
}

export default App
