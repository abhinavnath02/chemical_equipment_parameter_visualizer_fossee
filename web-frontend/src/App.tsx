import { useState, useEffect } from 'react'
import { AuthProvider, useAuth } from './context/AuthContext'
import { registerChartComponents } from './utils/chartConfig'
import AuthPage from './components/AuthPage'
import FileUpload from './components/FileUpload'
import UploadHistory from './components/UploadHistory'
import DataTable from './components/DataTable'
import ParameterBarChart from './components/charts/ParameterBarChart'
import EquipmentDoughnutChart from './components/charts/EquipmentDoughnutChart'
import EquipmentLineChart from './components/charts/EquipmentLineChart'
import CSVFormatGuide from './components/CSVFormatGuide'
import type { AnalysisResult, HistoryItem } from './types'
import './App.css'

registerChartComponents()

const API_BASE = 'http://127.0.0.1:8000/api'

function Dashboard() {
  const { accessToken, logout, user } = useAuth()
  const [file, setFile] = useState<File | null>(null)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  useEffect(() => {
    fetchHistory()
  }, [])

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_BASE}/upload/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      const data = await response.json()
      setResult(data)
      fetchHistory()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const fetchHistory = async () => {
    try {
      const response = await fetch(`${API_BASE}/history/`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      })
      const data = await response.json()
      setHistory(data)
    } catch (err) {
      console.error('Failed to fetch history:', err)
    }
  }

  const handleGeneratePDF = async () => {
    if (!result) return

    try {
      const response = await fetch(`${API_BASE}/generate-pdf/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify(result),
      })

      if (!response.ok) {
        throw new Error('PDF generation failed')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `equipment_report_${result.total_equipment}_items.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      console.error('Failed to generate PDF:', err)
      setError('Failed to generate PDF report')
    }
  }

  return (
    <div className="min-h-screen bg-black flex">
      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="border-b border-zinc-800 bg-black">
          <div className="px-6 py-4 flex justify-between items-center">
            <div>
              <h1 className="text-xl font-bold text-white">
                Chemical Equipment Parameter Visualizer
              </h1>
              <p className="text-gray-400 text-xs mt-1">Analyze and visualize equipment data</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-white">{user?.username}</p>
                <p className="text-xs text-gray-400">{user?.email}</p>
              </div>
              <button
                onClick={logout}
                className="bg-zinc-800 border border-zinc-700 text-white px-4 py-2 rounded-lg hover:bg-zinc-700 transition-colors text-sm font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto">
          <div className="max-w-7xl mx-auto px-6 py-6">
            {/* Upload Section - Full Width */}
            <div className="mb-6">
              <FileUpload
                file={file}
                loading={loading}
                error={error}
                onFileChange={handleFileChange}
                onUpload={handleUpload}
              />
            </div>

            {/* Summary Stats - Horizontal */}
            {result && (
              <div className="mb-6">
                <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="text-sm font-semibold text-white">Summary Statistics</h3>
                    <button
                      onClick={handleGeneratePDF}
                      className="bg-white text-black px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium flex items-center gap-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Download PDF
                    </button>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div className="bg-zinc-800 border border-zinc-700 p-3 rounded-lg">
                      <p className="text-xs text-gray-400 mb-1">Equipment</p>
                      <p className="text-xl font-bold text-white">{result.total_equipment}</p>
                    </div>
                    <div className="bg-zinc-800 border border-zinc-700 p-3 rounded-lg">
                      <p className="text-xs text-gray-400 mb-1">Flowrate</p>
                      <p className="text-xl font-bold text-white">{result.avg_flowrate.toFixed(1)}</p>
                    </div>
                    <div className="bg-zinc-800 border border-zinc-700 p-3 rounded-lg">
                      <p className="text-xs text-gray-400 mb-1">Pressure</p>
                      <p className="text-xl font-bold text-white">{result.avg_pressure.toFixed(1)}</p>
                    </div>
                    <div className="bg-zinc-800 border border-zinc-700 p-3 rounded-lg">
                      <p className="text-xs text-gray-400 mb-1">Temperature</p>
                      <p className="text-xl font-bold text-white">{result.avg_temperature.toFixed(1)}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Charts Section */}
            {result && (
              <div className="space-y-6 mb-6">
                {/* Data Table */}
                {result.equipment_data && (
                  <DataTable equipmentData={result.equipment_data} />
                )}

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <ParameterBarChart
                    avgFlowrate={result.avg_flowrate}
                    avgPressure={result.avg_pressure}
                    avgTemperature={result.avg_temperature}
                  />

                  {result.equipment_by_type && (
                    <EquipmentDoughnutChart equipmentByType={result.equipment_by_type} />
                  )}
                </div>

                {result.equipment_data && (
                  <EquipmentLineChart equipmentData={result.equipment_data} />
                )}
              </div>
            )}

            {/* CSV Format Guide - Collapsed by default */}
            <CSVFormatGuide />
          </div>
        </main>
      </div>

      {/* Sidebar for History */}
      <UploadHistory 
        history={history} 
        onRefresh={fetchHistory}
        isOpen={isSidebarOpen}
        onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
      />
    </div>
  )
}

function App() {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    )
  }

  return isAuthenticated ? <Dashboard /> : <AuthPage />
}

function AppWithAuth() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  )
}

export default AppWithAuth
