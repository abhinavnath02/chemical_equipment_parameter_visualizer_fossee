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

// Slider ranges for each parameter
const SLIDER_RANGES = {
  flowrate: { min: 0, max: 1000 },
  pressure: { min: 0, max: 2000 },
  temperature: { min: 0, max: 800 }
}

interface ThresholdSettingsProps {
  isOpen: boolean
  onClose: () => void
  onSave: (thresholds: Thresholds) => void
}

interface SliderInputProps {
  label: string
  value: number
  onChange: (value: number) => void
  min: number
  max: number
  accentColor: string
}

function SliderInput({ label, value, onChange, min, max, accentColor }: SliderInputProps) {
  const percentage = ((value - min) / (max - min)) * 100

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <label className="text-sm font-medium text-gray-400">{label}</label>
        <input
          type="number"
          value={value}
          onChange={(e) => {
            const num = parseFloat(e.target.value)
            if (!isNaN(num)) onChange(Math.max(min, Math.min(max, num)))
          }}
          className="w-20 bg-zinc-900 border border-zinc-600 rounded px-2 py-1 text-white text-sm text-right focus:outline-none focus:border-zinc-400"
        />
      </div>
      <div className="relative">
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onChange={(e) => onChange(parseFloat(e.target.value))}
          className="w-full h-2 rounded-lg appearance-none cursor-pointer slider-thumb"
          style={{
            background: `linear-gradient(to right, ${accentColor} 0%, ${accentColor} ${percentage}%, #3f3f46 ${percentage}%, #3f3f46 100%)`
          }}
        />
      </div>
    </div>
  )
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

  const updateThreshold = (param: keyof Thresholds, type: 'min' | 'max' | 'critical_max', value: number) => {
    setThresholds(prev => ({
      ...prev,
      [param]: {
        ...prev[param],
        [type]: value
      }
    }))
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
      <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-3xl">
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
            <div className="bg-zinc-800 border border-zinc-700 rounded-lg p-5">
              <h3 className="text-lg font-semibold text-red-400 mb-5 flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-red-400"></span>
                Flowrate Thresholds
              </h3>
              <div className="grid grid-cols-3 gap-6">
                <SliderInput
                  label="Minimum"
                  value={thresholds.flowrate.min}
                  onChange={(v) => updateThreshold('flowrate', 'min', v)}
                  min={SLIDER_RANGES.flowrate.min}
                  max={SLIDER_RANGES.flowrate.max}
                  accentColor="#f87171"
                />
                <SliderInput
                  label="Maximum"
                  value={thresholds.flowrate.max}
                  onChange={(v) => updateThreshold('flowrate', 'max', v)}
                  min={SLIDER_RANGES.flowrate.min}
                  max={SLIDER_RANGES.flowrate.max}
                  accentColor="#f87171"
                />
                <SliderInput
                  label="Critical Max"
                  value={thresholds.flowrate.critical_max}
                  onChange={(v) => updateThreshold('flowrate', 'critical_max', v)}
                  min={SLIDER_RANGES.flowrate.min}
                  max={SLIDER_RANGES.flowrate.max}
                  accentColor="#ef4444"
                />
              </div>
            </div>

            {/* Pressure Settings */}
            <div className="bg-zinc-800 border border-zinc-700 rounded-lg p-5">
              <h3 className="text-lg font-semibold text-blue-400 mb-5 flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-blue-400"></span>
                Pressure Thresholds
              </h3>
              <div className="grid grid-cols-3 gap-6">
                <SliderInput
                  label="Minimum"
                  value={thresholds.pressure.min}
                  onChange={(v) => updateThreshold('pressure', 'min', v)}
                  min={SLIDER_RANGES.pressure.min}
                  max={SLIDER_RANGES.pressure.max}
                  accentColor="#60a5fa"
                />
                <SliderInput
                  label="Maximum"
                  value={thresholds.pressure.max}
                  onChange={(v) => updateThreshold('pressure', 'max', v)}
                  min={SLIDER_RANGES.pressure.min}
                  max={SLIDER_RANGES.pressure.max}
                  accentColor="#60a5fa"
                />
                <SliderInput
                  label="Critical Max"
                  value={thresholds.pressure.critical_max}
                  onChange={(v) => updateThreshold('pressure', 'critical_max', v)}
                  min={SLIDER_RANGES.pressure.min}
                  max={SLIDER_RANGES.pressure.max}
                  accentColor="#3b82f6"
                />
              </div>
            </div>

            {/* Temperature Settings */}
            <div className="bg-zinc-800 border border-zinc-700 rounded-lg p-5">
              <h3 className="text-lg font-semibold text-green-400 mb-5 flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-green-400"></span>
                Temperature Thresholds
              </h3>
              <div className="grid grid-cols-3 gap-6">
                <SliderInput
                  label="Minimum"
                  value={thresholds.temperature.min}
                  onChange={(v) => updateThreshold('temperature', 'min', v)}
                  min={SLIDER_RANGES.temperature.min}
                  max={SLIDER_RANGES.temperature.max}
                  accentColor="#4ade80"
                />
                <SliderInput
                  label="Maximum"
                  value={thresholds.temperature.max}
                  onChange={(v) => updateThreshold('temperature', 'max', v)}
                  min={SLIDER_RANGES.temperature.min}
                  max={SLIDER_RANGES.temperature.max}
                  accentColor="#4ade80"
                />
                <SliderInput
                  label="Critical Max"
                  value={thresholds.temperature.critical_max}
                  onChange={(v) => updateThreshold('temperature', 'critical_max', v)}
                  min={SLIDER_RANGES.temperature.min}
                  max={SLIDER_RANGES.temperature.max}
                  accentColor="#22c55e"
                />
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

      {/* Custom slider styles */}
      <style>{`
        .slider-thumb::-webkit-slider-thumb {
          -webkit-appearance: none;
          appearance: none;
          width: 18px;
          height: 18px;
          border-radius: 50%;
          background: #ffffff;
          cursor: pointer;
          border: 2px solid #71717a;
          box-shadow: 0 2px 4px rgba(0,0,0,0.3);
          transition: transform 0.1s;
        }
        .slider-thumb::-webkit-slider-thumb:hover {
          transform: scale(1.1);
        }
        .slider-thumb::-moz-range-thumb {
          width: 18px;
          height: 18px;
          border-radius: 50%;
          background: #ffffff;
          cursor: pointer;
          border: 2px solid #71717a;
          box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
      `}</style>
    </>
  )
}
