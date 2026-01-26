import { useState } from 'react'

export default function CSVFormatGuide() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex justify-between items-center p-4 hover:bg-zinc-800 transition-colors"
      >
        <h2 className="text-sm font-semibold text-white">CSV Format Guide</h2>
        <svg
          className={`w-5 h-5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      
      {isOpen && (
        <div className="px-4 pb-4 border-t border-zinc-800">
          <p className="text-gray-400 text-sm mb-3 mt-3">
            Your CSV file should include the following columns:
          </p>
          <div className="bg-black border border-zinc-800 p-3 rounded-lg font-mono text-xs overflow-x-auto">
            <code className="text-gray-300">
              <span className="text-gray-500">Equipment Name,Type,Flowrate,Pressure,Temperature</span>
              <br />
              Pump-1,Pump,120,5.2,110
              <br />
              Compressor-1,Compressor,95,8.4,95
              <br />
              Valve-1,Valve,60,4.1,105
            </code>
          </div>
        </div>
      )}
    </div>
  )
}
