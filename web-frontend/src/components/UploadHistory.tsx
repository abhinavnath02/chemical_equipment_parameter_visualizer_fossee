import { useState } from 'react'

interface HistoryItem {
  id: number
  filename: string
  uploaded_at: string
  total_equipment: number
}

interface UploadHistoryProps {
  history: HistoryItem[]
  onRefresh: () => void
  onHistoryClick: (id: number) => void
  isOpen: boolean
  onToggle: () => void
  equipmentData?: Array<{
    name: string
    type: string
    flowrate: number
    pressure: number
    temperature: number
  }>
  thresholds?: {
    flowrate: { min: number; max: number; critical_max: number }
    pressure: { min: number; max: number; critical_max: number }
    temperature: { min: number; max: number; critical_max: number }
  }
}

const DEFAULT_THRESHOLDS = {
  flowrate: { min: 50, max: 500, critical_max: 600 },
  pressure: { min: 100, max: 800, critical_max: 1000 },
  temperature: { min: 50, max: 350, critical_max: 400 }
}

export default function UploadHistory({ 
  history, 
  onRefresh, 
  onHistoryClick, 
  isOpen, 
  onToggle,
  equipmentData = [],
  thresholds = DEFAULT_THRESHOLDS
}: UploadHistoryProps) {
  
  const [isWarningsExpanded, setIsWarningsExpanded] = useState(false)
  
  const checkEquipmentAlerts = () => {
    if (!equipmentData || equipmentData.length === 0) {
      return []
    }

    const alerts: Array<{
      equipment: string
      type: string
      level: 'warning' | 'critical'
      messages: string[]
    }> = []

    equipmentData.forEach(eq => {
      const messages: string[] = []
      let level: 'warning' | 'critical' = 'warning'

      // Check flowrate
      if (eq.flowrate > thresholds.flowrate.critical_max) {
        messages.push(`🔴 Flowrate ${eq.flowrate.toFixed(1)} exceeds critical limit ${thresholds.flowrate.critical_max}`)
        level = 'critical'
      } else if (eq.flowrate > thresholds.flowrate.max) {
        messages.push(`⚠️ Flowrate ${eq.flowrate.toFixed(1)} exceeds safe maximum ${thresholds.flowrate.max}`)
      } else if (eq.flowrate < thresholds.flowrate.min) {
        messages.push(`⚠️ Flowrate ${eq.flowrate.toFixed(1)} below safe minimum ${thresholds.flowrate.min}`)
      }

      // Check pressure
      if (eq.pressure > thresholds.pressure.critical_max) {
        messages.push(`🔴 Pressure ${eq.pressure.toFixed(1)} exceeds critical limit ${thresholds.pressure.critical_max}`)
        level = 'critical'
      } else if (eq.pressure > thresholds.pressure.max) {
        messages.push(`⚠️ Pressure ${eq.pressure.toFixed(1)} exceeds safe maximum ${thresholds.pressure.max}`)
      } else if (eq.pressure < thresholds.pressure.min) {
        messages.push(`⚠️ Pressure ${eq.pressure.toFixed(1)} below safe minimum ${thresholds.pressure.min}`)
      }

      // Check temperature
      if (eq.temperature > thresholds.temperature.critical_max) {
        messages.push(`🔴 Temperature ${eq.temperature.toFixed(1)} exceeds critical limit ${thresholds.temperature.critical_max}`)
        level = 'critical'
      } else if (eq.temperature > thresholds.temperature.max) {
        messages.push(`⚠️ Temperature ${eq.temperature.toFixed(1)} exceeds safe maximum ${thresholds.temperature.max}`)
      } else if (eq.temperature < thresholds.temperature.min) {
        messages.push(`⚠️ Temperature ${eq.temperature.toFixed(1)} below safe minimum ${thresholds.temperature.min}`)
      }

      if (messages.length > 0) {
        alerts.push({
          equipment: eq.name,
          type: eq.type,
          level,
          messages
        })
      }
    })

    return alerts
  }
  
  const checkSafetyStatus = () => {
    if (!equipmentData || equipmentData.length === 0) {
      return { safe: 0, warning: 0, critical: 0, total: 0 }
    }

    let safe = 0
    let warning = 0
    let critical = 0

    equipmentData.forEach(eq => {
      let hasCritical = false
      let hasWarning = false

      // Check flowrate
      if (eq.flowrate > thresholds.flowrate.critical_max) {
        hasCritical = true
      } else if (eq.flowrate > thresholds.flowrate.max || eq.flowrate < thresholds.flowrate.min) {
        hasWarning = true
      }

      // Check pressure
      if (eq.pressure > thresholds.pressure.critical_max) {
        hasCritical = true
      } else if (eq.pressure > thresholds.pressure.max || eq.pressure < thresholds.pressure.min) {
        hasWarning = true
      }

      // Check temperature
      if (eq.temperature > thresholds.temperature.critical_max) {
        hasCritical = true
      } else if (eq.temperature > thresholds.temperature.max || eq.temperature < thresholds.temperature.min) {
        hasWarning = true
      }

      if (hasCritical) {
        critical++
      } else if (hasWarning) {
        warning++
      } else {
        safe++
      }
    })

    return { safe, warning, critical, total: equipmentData.length }
  }

  const alerts = checkEquipmentAlerts()
  const safetyStatus = checkSafetyStatus()
  const criticalCount = alerts.filter(a => a.level === 'critical').length
  const warningCount = alerts.filter(a => a.level === 'warning').length

  return (
    <>
      {/* Mobile/Tablet Toggle Button */}
      <button
        onClick={onToggle}
        className="lg:hidden fixed top-20 right-4 z-50 bg-zinc-900 border border-zinc-700 text-white p-3 rounded-lg shadow-lg hover:bg-zinc-800 transition-colors"
      >
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>

      {/* Sidebar */}
      <div
        className={`fixed lg:relative top-0 right-0 h-screen bg-zinc-900 border-l border-zinc-800 transition-transform duration-300 z-40 flex flex-col ${
          isOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0'
        } w-80`}
      >
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b border-zinc-800 flex-shrink-0">
          <h2 className="text-lg font-semibold text-white">Recent Uploads</h2>
          <div className="flex items-center gap-2">
            <button
              onClick={onRefresh}
              className="text-gray-400 hover:text-white transition-colors p-1"
              title="Refresh"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
            <button
              onClick={onToggle}
              className="lg:hidden text-gray-400 hover:text-white transition-colors p-1"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* History List */}
        <div className="flex-1 overflow-y-auto p-4">
          {history.length === 0 ? (
            <p className="text-gray-500 text-center py-8 text-sm">
              No uploads yet
            </p>
          ) : (
            <div className="space-y-2">
              {history.map((item, index) => (
                <div
                  key={index}
                  onClick={() => onHistoryClick(item.id)}
                  className="border border-zinc-800 rounded-lg p-3 hover:bg-zinc-800 transition-colors cursor-pointer"
                >
                  <div className="flex justify-between items-start gap-2">
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-white text-sm truncate">
                        {item.filename}
                      </p>
                      <p className="text-xs text-gray-400 mt-1">
                        {new Date(item.uploaded_at).toLocaleDateString()} {new Date(item.uploaded_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                    <span className="bg-zinc-800 border border-zinc-700 text-gray-300 text-xs font-medium px-2 py-0.5 rounded whitespace-nowrap">
                      {item.total_equipment}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Safety Warnings Section */}
        {safetyStatus.total > 0 && (
          <div className="border-t border-zinc-800 flex-shrink-0">
            {/* Summary Header - Collapsible */}
            <button
              onClick={() => setIsWarningsExpanded(!isWarningsExpanded)}
              className="w-full p-4 flex items-center justify-between hover:bg-zinc-800/50 transition-colors"
            >
              <div className="flex items-center gap-3 flex-1">
                {alerts.length === 0 ? (
                  <>
                    <svg className="w-5 h-5 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div className="text-left">
                      <p className="text-green-400 font-semibold text-xs">All Systems Normal</p>
                      <p className="text-green-300 text-xs mt-0.5">{safetyStatus.safe} equipment safe</p>
                    </div>
                  </>
                ) : (
                  <>
                    <svg className={`w-5 h-5 flex-shrink-0 ${criticalCount > 0 ? 'text-red-400' : 'text-yellow-400'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <div className="text-left flex-1 min-w-0">
                      <p className={`${criticalCount > 0 ? 'text-red-400' : 'text-yellow-400'} font-semibold text-xs`}>
                        {criticalCount > 0 && <span>{criticalCount} Critical</span>}
                        {criticalCount > 0 && warningCount > 0 && <span> • </span>}
                        {warningCount > 0 && <span>{warningCount} Warning{warningCount > 1 ? 's' : ''}</span>}
                      </p>
                      <p className="text-gray-400 text-xs mt-0.5">{safetyStatus.safe} safe</p>
                    </div>
                  </>
                )}
              </div>
              {alerts.length > 0 && (
                <svg
                  className={`w-4 h-4 text-gray-400 transition-transform flex-shrink-0 ${isWarningsExpanded ? 'rotate-180' : ''}`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              )}
            </button>

            {/* Expanded Warnings List */}
            {isWarningsExpanded && alerts.length > 0 && (
              <div className="max-h-96 overflow-y-auto border-t border-zinc-800">
                <div className="p-3 space-y-2">
                  {alerts.map((alert, idx) => (
                    <div
                      key={idx}
                      className={`${alert.level === 'critical' ? 'bg-red-500/5 border-red-500/30' : 'bg-yellow-500/5 border-yellow-500/30'} border rounded-lg p-2`}
                    >
                      <div className="flex items-start gap-2">
                        <div className={`flex-shrink-0 w-1.5 h-1.5 rounded-full mt-1.5 ${alert.level === 'critical' ? 'bg-red-500 animate-pulse' : 'bg-yellow-500'}`}></div>
                        <div className="flex-1 min-w-0">
                          <p className="text-white font-semibold text-xs truncate" title={alert.equipment}>
                            {alert.equipment}
                          </p>
                          <p className="text-gray-400 text-xs mb-1">{alert.type}</p>
                          <div className="space-y-0.5">
                            {alert.messages.map((msg, msgIdx) => (
                              <p key={msgIdx} className={`text-xs ${alert.level === 'critical' ? 'text-red-300' : 'text-yellow-300'}`}>
                                {msg}
                              </p>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
          onClick={onToggle}
        />
      )}
    </>
  )
}
