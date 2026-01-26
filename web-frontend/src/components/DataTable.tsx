interface DataTableProps {
  equipmentData: Array<{
    name: string
    type: string
    flowrate: number
    pressure: number
    temperature: number
  }>
}

export default function DataTable({ equipmentData }: DataTableProps) {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden">
      <div className="p-4 border-b border-zinc-800">
        <h3 className="text-lg font-semibold text-white">Equipment Data</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-zinc-800 border-b border-zinc-700">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                Equipment Name
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                Type
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                Flowrate
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                Pressure
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                Temperature
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800">
            {equipmentData.map((item, index) => (
              <tr key={index} className="hover:bg-zinc-800 transition-colors">
                <td className="px-4 py-3 text-white">{item.name}</td>
                <td className="px-4 py-3 text-gray-300">{item.type}</td>
                <td className="px-4 py-3 text-gray-300">{item.flowrate}</td>
                <td className="px-4 py-3 text-gray-300">{item.pressure}</td>
                <td className="px-4 py-3 text-gray-300">{item.temperature}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
