interface SafetyAlertsProps {
  equipmentData: Array<{
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

interface Alert {
  equipment: string
  type: string
  level: 'warning' | 'critical'
  messages: string[]
}

export default function SafetyAlerts({ equipmentData, thresholds = DEFAULT_THRESHOLDS }: SafetyAlertsProps) {
  const checkEquipment = () => {
    const alerts: Alert[] = []

    equipmentData.forEach(eq => {
      const messages: string[] = []
      let level: 'warning' | 'critical' = 'warning'

      // Check flowrate
      if (eq.flowrate > thresholds.flowrate.critical_max) {
        messages.push(`🔴 CRITICAL: Flowrate ${eq.flowrate.toFixed(1)} exceeds critical limit ${thresholds.flowrate.critical_max}`)
        level = 'critical'
      } else if (eq.flowrate > thresholds.flowrate.max) {
        messages.push(`⚠️ Flowrate ${eq.flowrate.toFixed(1)} exceeds safe maximum ${thresholds.flowrate.max}`)
      } else if (eq.flowrate < thresholds.flowrate.min) {
        messages.push(`⚠️ Flowrate ${eq.flowrate.toFixed(1)} below safe minimum ${thresholds.flowrate.min}`)
      }

      // Check pressure
      if (eq.pressure > thresholds.pressure.critical_max) {
        messages.push(`🔴 CRITICAL: Pressure ${eq.pressure.toFixed(1)} exceeds critical limit ${thresholds.pressure.critical_max}`)
        level = 'critical'
      } else if (eq.pressure > thresholds.pressure.max) {
        messages.push(`⚠️ Pressure ${eq.pressure.toFixed(1)} exceeds safe maximum ${thresholds.pressure.max}`)
      } else if (eq.pressure < thresholds.pressure.min) {
        messages.push(`⚠️ Pressure ${eq.pressure.toFixed(1)} below safe minimum ${thresholds.pressure.min}`)
      }

      // Check temperature
      if (eq.temperature > thresholds.temperature.critical_max) {
        messages.push(`🔴 CRITICAL: Temperature ${eq.temperature.toFixed(1)} exceeds critical limit ${thresholds.temperature.critical_max}`)
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

  const alerts = checkEquipment()
  const criticalCount = alerts.filter(a => a.level === 'critical').length
  const warningCount = alerts.filter(a => a.level === 'warning').length

  if (alerts.length === 0) {
    return (
      <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
        <div className="flex items-center gap-3">
          <div className="flex-shrink-0">
            <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h3 className="text-green-400 font-semibold text-lg">All Systems Normal</h3>
            <p className="text-green-300 text-sm mt-1">
              All equipment operating within safe parameters
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Summary Banner */}
      <div className={`${criticalCount > 0 ? 'bg-red-500/10 border-red-500/30' : 'bg-yellow-500/10 border-yellow-500/30'} border rounded-lg p-4`}>
        <div className="flex items-center gap-3">
          <div className="flex-shrink-0">
            {criticalCount > 0 ? (
              <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            ) : (
              <svg className="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            )}
          </div>
          <div className="flex-1">
            <h3 className={`${criticalCount > 0 ? 'text-red-400' : 'text-yellow-400'} font-semibold text-lg`}>
              Safety Alerts Detected
            </h3>
            <p className={`${criticalCount > 0 ? 'text-red-300' : 'text-yellow-300'} text-sm mt-1`}>
              {criticalCount > 0 && <span className="font-semibold">{criticalCount} Critical Alert{criticalCount > 1 ? 's' : ''}</span>}
              {criticalCount > 0 && warningCount > 0 && <span> • </span>}
              {warningCount > 0 && <span>{warningCount} Warning{warningCount > 1 ? 's' : ''}</span>}
              {' '}— Immediate attention required
            </p>
          </div>
        </div>
      </div>

      {/* Alert Details */}
      <div className="space-y-3">
        {alerts.map((alert, idx) => (
          <div 
            key={idx}
            className={`${alert.level === 'critical' ? 'bg-red-500/5 border-red-500/30' : 'bg-yellow-500/5 border-yellow-500/30'} border rounded-lg p-4`}
          >
            <div className="flex items-start gap-3">
              <div className={`flex-shrink-0 w-2 h-2 rounded-full mt-2 ${alert.level === 'critical' ? 'bg-red-500 animate-pulse' : 'bg-yellow-500'}`}></div>
              <div className="flex-1">
                <h4 className="text-white font-semibold">
                  {alert.equipment} 
                  <span className="text-gray-400 font-normal text-sm ml-2">({alert.type})</span>
                </h4>
                <ul className="mt-2 space-y-1">
                  {alert.messages.map((msg, msgIdx) => (
                    <li key={msgIdx} className={`text-sm ${alert.level === 'critical' ? 'text-red-300' : 'text-yellow-300'}`}>
                      {msg}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
