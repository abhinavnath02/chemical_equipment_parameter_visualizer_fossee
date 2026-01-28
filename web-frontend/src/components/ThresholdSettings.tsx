import { useState, useEffect } from 'react'

interface Thresholds {
  flowrate: { min: number; max: number; critical_max: number }
  pressure: { min: number; max: number; critical_max: number }
  temperature: { min: number; max: number; critical_max: number }
}

const DEFAULT_THRESHOLDS: Thresholds = {
  flowrate: { min: 50, max: 500, critical_max: 600 },
  pressure: { min: 100, max: 800, critical_max: 1000 },
  temperature: { min: 50, max: 350, critical_max: 400 }
}

interface ThresholdSettingsProps {
  isOpen: boolean
  onClose: () => void
  onSave: (thresholds: Thresholds) => void
}

export default function ThresholdSettings({ isOpen, onClose, onSave }: ThresholdSettingsProps) {
  const [thresholds, setThresholds] = useState<Thresholds>(DEFAULT_THRESHOLDS)

  useEffect(() => {
    // Load from localStorage
    const saved = localStorage.getItem('safety_thresholds')
    if (saved) {
      setThresholds(JSON.parse(saved))
    }
  }, [])

  const handleSave = () => {
    localStorage.setItem('safety_thresholds', JSON.stringify(thresholds))
    onSave(thresholds)
    onClose()
  }

  const handleReset = () => {
    setThresholds(DEFAULT_THRESHOLDS)
  }

  const updateThreshold = (param: keyof Thresholds, type: 'min' | 'max' | 'critical_max', value: string) => {
    const numValue = parseFloat(value)
    if (!isNaN(numValue)) {
      setThresholds(prev => ({
        ...prev,
        [param]: {
          ...prev[param],
          [type]: numValue
        }
      }))
    }
  }

  if (!isOpen) return null

  return (
    <>
      {/* Overlay */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-70 z-50"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-2xl">
        <div className="bg-zinc-900 border border-zinc-700 rounded-xl shadow-2xl max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="border-b border-zinc-800 px-6 py-4 flex justify-between items-center">
            <div>
              <h2 className="text-xl font-bold text-white">Safety Threshold Settings</h2>
              <p className="text-sm text-gray-400 mt-1">Configure warning and critical limits for equipment parameters</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Content */}
          <div className="p-6 space-y-6">
            {/* Info Banner */}
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
              <div className="flex gap-3">
                <svg className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div className="text-sm text-gray-300">
                  <p className="font-semibold text-blue-400 mb-1">How it works:</p>
                  <ul className="list-disc list-inside space-y-1">
                    <li><span className="text-green-400">Safe</span>: Values between Min and Max</li>
                    <li><span className="text-yellow-400">Warning</span>: Values outside Min-Max range but below Critical</li>
                    <li><span className="text-red-400">Critical</span>: Values above Critical Max</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Flowrate Settings */}
            <div className="bg-zinc-800 border border-zinc-700 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-red-400 mb-4 flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-red-400"></span>
                Flowrate Thresholds
              </h3>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Minimum</label>
                  <input
                    type="number"
                    value={thresholds.flowrate.min}
                    onChange={(e) => updateThreshold('flowrate', 'min', e.target.value)}
                    className="w-full bg-zinc-900 border border-zinc-600 rounded px-3 py-2 text-white focus:outline-none focus:border-red-400"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Maximum</label>
                  <input
                    type="number"
                    value={thresholds.flowrate.max}
                    onChange={(e) => updateThreshold('flowrate', 'max', e.target.value)}
                    className="w-full bg-zinc-900 border border-zinc-600 rounded px-3 py-2 text-white focus:outline-none focus:border-red-400"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Critical Max</label>
                  <input
                    type="number"
                    value={thresholds.flowrate.critical_max}
                    onChange={(e) => updateThreshold('flowrate', 'critical_max', e.target.value)}
                    className="w-full bg-zinc-900 border border-zinc-600 rounded px-3 py-2 text-white focus:outline-none focus:border-red-400"
                  />
                </div>
              </div>
            </div>

            {/* Pressure Settings */}
            <div className="bg-zinc-800 border border-zinc-700 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-blue-400 mb-4 flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-blue-400"></span>
                Pressure Thresholds
              </h3>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Minimum</label>
                  <input
                    type="number"
                    value={thresholds.pressure.min}
                    onChange={(e) => updateThreshold('pressure', 'min', e.target.value)}
                    className="w-full bg-zinc-900 border border-zinc-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-400"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Maximum</label>
                  <input
                    type="number"
                    value={thresholds.pressure.max}
                    onChange={(e) => updateThreshold('pressure', 'max', e.target.value)}
                    className="w-full bg-zinc-900 border border-zinc-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-400"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Critical Max</label>
                  <input
                    type="number"
                    value={thresholds.pressure.critical_max}
                    onChange={(e) => updateThreshold('pressure', 'critical_max', e.target.value)}
                    className="w-full bg-zinc-900 border border-zinc-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-400"
                  />
                </div>
              </div>
            </div>

            {/* Temperature Settings */}
            <div className="bg-zinc-800 border border-zinc-700 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-green-400 mb-4 flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-green-400"></span>
                Temperature Thresholds
              </h3>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Minimum</label>
                  <input
                    type="number"
                    value={thresholds.temperature.min}
                    onChange={(e) => updateThreshold('temperature', 'min', e.target.value)}
                    className="w-full bg-zinc-900 border border-zinc-600 rounded px-3 py-2 text-white focus:outline-none focus:border-green-400"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Maximum</label>
                  <input
                    type="number"
                    value={thresholds.temperature.max}
                    onChange={(e) => updateThreshold('temperature', 'max', e.target.value)}
                    className="w-full bg-zinc-900 border border-zinc-600 rounded px-3 py-2 text-white focus:outline-none focus:border-green-400"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">Critical Max</label>
                  <input
                    type="number"
                    value={thresholds.temperature.critical_max}
                    onChange={(e) => updateThreshold('temperature', 'critical_max', e.target.value)}
                    className="w-full bg-zinc-900 border border-zinc-600 rounded px-3 py-2 text-white focus:outline-none focus:border-green-400"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="border-t border-zinc-800 px-6 py-4 flex justify-between">
            <button
              onClick={handleReset}
              className="px-4 py-2 bg-zinc-800 border border-zinc-700 text-white rounded-lg hover:bg-zinc-700 transition-colors"
            >
              Reset to Defaults
            </button>
            <div className="flex gap-3">
              <button
                onClick={onClose}
                className="px-4 py-2 bg-zinc-800 border border-zinc-700 text-white rounded-lg hover:bg-zinc-700 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Save Settings
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
