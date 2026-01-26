import { Doughnut } from 'react-chartjs-2'

interface EquipmentDoughnutChartProps {
  equipmentByType: { [key: string]: number }
}

export default function EquipmentDoughnutChart({
  equipmentByType,
}: EquipmentDoughnutChartProps) {
  const data = {
    labels: Object.keys(equipmentByType),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(equipmentByType),
        backgroundColor: [
          'rgba(59, 130, 246, 0.6)',
          'rgba(16, 185, 129, 0.6)',
          'rgba(249, 115, 22, 0.6)',
          'rgba(168, 85, 247, 0.6)',
          'rgba(236, 72, 153, 0.6)',
          'rgba(34, 197, 94, 0.6)',
        ],
        borderColor: [
          'rgb(59, 130, 246)',
          'rgb(16, 185, 129)',
          'rgb(249, 115, 22)',
          'rgb(168, 85, 247)',
          'rgb(236, 72, 153)',
          'rgb(34, 197, 94)',
        ],
        borderWidth: 2,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          color: '#9CA3AF',
          padding: 15,
        },
      },
    },
  }

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
      <h3 className="text-lg font-semibold mb-6 text-white">Equipment Distribution</h3>
      <div className="flex justify-center">
        <div className="w-64 h-64">
          <Doughnut data={data} options={options} />
        </div>
      </div>
    </div>
  )
}
