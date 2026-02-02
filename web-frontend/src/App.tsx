import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { registerChartComponents } from './utils/chartConfig'
import LandingPage from './components/LandingPage'
import AuthPage from './components/AuthPage'
import FileUpload from './components/FileUpload'
import UploadHistory from './components/UploadHistory'
import DataTable from './components/DataTable'
import ParameterBarChart from './components/charts/ParameterBarChart'
import EquipmentDoughnutChart from './components/charts/EquipmentDoughnutChart'
import EquipmentLineChart from './components/charts/EquipmentLineChart'
import SafetyStatusChart from './components/charts/SafetyStatusChart'
import ParameterDistributionChart from './components/charts/ParameterDistributionChart'
import CSVFormatGuide from './components/CSVFormatGuide'
import ThresholdSettings from './components/ThresholdSettings'
import SmartInsights from './components/SmartInsights'
import type { AnalysisResult, HistoryItem } from './types'
import './App.css'

registerChartComponents()

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

function Dashboard() {
  const { accessToken, logout, user } = useAuth()
  const navigate = useNavigate()
  const [file, setFile] = useState<File | null>(null)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)
  const [thresholds, setThresholds] = useState({
    flowrate: { min: 50, max: 500, critical_max: 600 },
    pressure: { min: 100, max: 800, critical_max: 1000 },
    temperature: { min: 50, max: 350, critical_max: 400 }
  })

  useEffect(() => {
    fetchHistory()
    // Load thresholds from localStorage
    const saved = localStorage.getItem('safety_thresholds')
    if (saved) {
      setThresholds(JSON.parse(saved))
    }
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

  const handleHistoryClick = async (datasetId: number) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_BASE}/dataset/${datasetId}/`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      })
      
      if (!response.ok) {
        throw new Error('Failed to fetch dataset')
      }
      
      const data = await response.json()
      setResult(data)
      setIsSidebarOpen(false) // Close sidebar on mobile after selection
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load dataset')
    } finally {
      setLoading(false)
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
    <div className="h-screen bg-black flex relative overflow-hidden">
      {/* Rainbow gradient border */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-gradient-to-br from-red-500/15 to-transparent blur-3xl"></div>
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-gradient-to-bl from-blue-500/15 to-transparent blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-gradient-to-tr from-purple-500/15 to-transparent blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-gradient-to-tl from-green-500/15 to-transparent blur-3xl"></div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative z-10 min-w-0">
        {/* Header */}
        <header className="border-b border-zinc-800 bg-black flex-shrink-0">
          <div className="px-6 py-4 flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/')}
                className="text-gray-400 hover:text-white transition-colors"
                title="Back to Home"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
              </button>
              <div>
                <h1 className="text-xl font-bold text-white">
                  Chemical Equipment Parameter Visualizer
                </h1>
                <p className="text-gray-400 text-xs mt-1">Analyze and visualize equipment data</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setIsSettingsOpen(true)}
                className="bg-zinc-800 border border-zinc-700 text-white px-4 py-2 rounded-lg hover:bg-zinc-700 transition-colors text-sm font-medium flex items-center gap-2"
                title="Safety Threshold Settings"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Settings
              </button>
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

            {/* Smart Insights Section */}
            {result && result.smart_insights && (
              <SmartInsights insights={result.smart_insights} />
            )}

            {/* Charts Section */}
            {result && (
              <div className="space-y-6 mb-6">
                {/* Main Analytics Charts */}
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

                {/* Safety Status Chart */}
                {result.equipment_data && (
                  <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4" style={{ height: '400px' }}>
                    <SafetyStatusChart equipmentData={result.equipment_data} thresholds={thresholds} />
                  </div>
                )}

                {/* Equipment Trend Line Chart */}
                {result.equipment_data && (
                  <EquipmentLineChart equipmentData={result.equipment_data} />
                )}

                {/* Parameter Distribution Histograms */}
                {result.equipment_data && (
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4" style={{ height: '300px' }}>
                      <ParameterDistributionChart equipmentData={result.equipment_data} parameter="flowrate" thresholds={thresholds} />
                    </div>
                    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4" style={{ height: '300px' }}>
                      <ParameterDistributionChart equipmentData={result.equipment_data} parameter="pressure" thresholds={thresholds} />
                    </div>
                    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4" style={{ height: '300px' }}>
                      <ParameterDistributionChart equipmentData={result.equipment_data} parameter="temperature" thresholds={thresholds} />
                    </div>
                  </div>
                )}

                {/* Data Table */}
                {result.equipment_data && (
                  <DataTable equipmentData={result.equipment_data} />
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
        onHistoryClick={handleHistoryClick}
        isOpen={isSidebarOpen}
        onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
        equipmentData={result?.equipment_data}
        thresholds={thresholds}
      />

      {/* Threshold Settings Modal */}
      <ThresholdSettings
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onSave={(newThresholds) => {
          setThresholds(newThresholds)
          console.log('Thresholds updated:', newThresholds)
        }}
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

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route 
        path="/app" 
        element={isAuthenticated ? <Dashboard /> : <AuthPage />} 
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

function AppWithAuth() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  )
}

export default AppWithAuth
