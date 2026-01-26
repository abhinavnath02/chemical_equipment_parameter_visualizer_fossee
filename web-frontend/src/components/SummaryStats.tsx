interface SummaryStatsProps {
  totalEquipment: number
  avgFlowrate: number
  avgPressure: number
  avgTemperature: number
}

export default function SummaryStats({
  totalEquipment,
  avgFlowrate,
  avgPressure,
  avgTemperature,
}: SummaryStatsProps) {
  return (
    <div className="mt-6 border-t border-zinc-800 pt-6">
      <h3 className="text-lg font-semibold mb-4 text-white">Summary Statistics</h3>
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-zinc-800 border border-zinc-700 p-4 rounded-lg">
          <p className="text-xs text-gray-400 mb-1">Equipment</p>
          <p className="text-2xl font-bold text-white">{totalEquipment}</p>
        </div>
        <div className="bg-zinc-800 border border-zinc-700 p-4 rounded-lg">
          <p className="text-xs text-gray-400 mb-1">Flowrate</p>
          <p className="text-2xl font-bold text-white">
            {avgFlowrate.toFixed(1)}
          </p>
        </div>
        <div className="bg-zinc-800 border border-zinc-700 p-4 rounded-lg">
          <p className="text-xs text-gray-400 mb-1">Pressure</p>
          <p className="text-2xl font-bold text-white">
            {avgPressure.toFixed(1)}
          </p>
        </div>
        <div className="bg-zinc-800 border border-zinc-700 p-4 rounded-lg">
          <p className="text-xs text-gray-400 mb-1">Temperature</p>
          <p className="text-2xl font-bold text-white">
            {avgTemperature.toFixed(1)}
          </p>
        </div>
      </div>
    </div>
  )
}
