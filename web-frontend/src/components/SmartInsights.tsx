import type { AnalysisResult } from '../types'

interface SmartInsightsProps {
  insights: NonNullable<AnalysisResult['smart_insights']>
}

export default function SmartInsights({ insights }: SmartInsightsProps) {
  if (!insights) return null

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pb-6">
      {/* Correlations Card */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
        <div className="flex items-center gap-2 mb-4">
          <div className="p-2 bg-purple-500/20 rounded-lg">
            <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div>
            <h3 className="font-semibold text-white">Parameter Correlations</h3>
            <p className="text-xs text-gray-400">Relationships between variables</p>
          </div>
        </div>

        <div className="space-y-3">
          {insights.correlations.length > 0 ? (
            insights.correlations.map((corr, idx) => (
              <div key={idx} className="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700/50">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-zinc-200 font-medium">{corr.pair}</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                    corr.value > 0 ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'
                  }`}>
                    {Math.abs(corr.value).toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-zinc-500">{corr.interpretation} Correlation</span>
                  <div className="w-20 h-1 bg-zinc-700 rounded-full overflow-hidden">
                    <div 
                      className={`h-full ${corr.value > 0 ? 'bg-green-500' : 'bg-red-500'}`} 
                      style={{ width: `${Math.abs(corr.value) * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-zinc-500 text-sm text-center py-4">No significant correlations found.</p>
          )}
        </div>
      </div>

      {/* Outliers Card */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
        <div className="flex items-center gap-2 mb-4">
          <div className="p-2 bg-orange-500/20 rounded-lg">
            <svg className="w-5 h-5 text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <h3 className="font-semibold text-white">Statistical Deviations</h3>
            <p className="text-xs text-gray-400">Z-Score anomalies ({'>'} 2σ)</p>
          </div>
        </div>

        <div className="space-y-3 max-h-64 overflow-y-auto pr-1 custom-scrollbar">
          {insights.outliers.length > 0 ? (
            insights.outliers.map((item, idx) => (
              <div key={idx} className="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700/50 flex items-start gap-3">
                <span className="mt-1 text-orange-400 text-xs font-mono">{item.deviation}</span>
                <div className="flex-1">
                  <div className="flex justify-between">
                    <span className="text-zinc-200 font-medium text-sm">{item.equipment}</span>
                    <span className="text-white font-bold text-sm">{item.value.toFixed(1)}</span>
                  </div>
                  <div className="flex justify-between items-center mt-1">
                    <span className="text-xs text-zinc-500 uppercase">{item.parameter}</span>
                    <span className="text-xs text-zinc-600">Avg: {item.mean}</span>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="flex flex-col items-center justify-center py-8 text-zinc-500 gap-2">
              <svg className="w-8 h-8 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-sm">No statistical anomalies detected.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
