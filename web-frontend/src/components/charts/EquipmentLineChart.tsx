import { Line } from 'react-chartjs-2'

interface EquipmentData {
  name: string
  type: string
  flowrate: number
  pressure: number
  temperature: number
}

interface EquipmentLineChartProps {
  equipmentData: EquipmentData[]
}

export default function EquipmentLineChart({ equipmentData }: EquipmentLineChartProps) {
  const data = {
    labels: equipmentData.map((eq) => eq.name),
    datasets: [
      {
        label: 'Flowrate',
        data: equipmentData.map((eq) => eq.flowrate),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        tension: 0.4,
      },
      {
        label: 'Pressure',
        data: equipmentData.map((eq) => eq.pressure),
        borderColor: 'rgb(168, 85, 247)',
        backgroundColor: 'rgba(168, 85, 247, 0.5)',
        tension: 0.4,
      },
      {
        label: 'Temperature',
        data: equipmentData.map((eq) => eq.temperature),
        borderColor: 'rgb(249, 115, 22)',
        backgroundColor: 'rgba(249, 115, 22, 0.5)',
        tension: 0.4,
      },
    ],
  }

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: '#9CA3AF',
          padding: 15,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: '#9CA3AF',
        },
      },
      x: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: '#9CA3AF',
        },
      },
    },
  }

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
      <h3 className="text-lg font-semibold mb-6 text-white">Equipment Parameter Comparison</h3>
      <Line data={data} options={options} />
    </div>
  )
}
