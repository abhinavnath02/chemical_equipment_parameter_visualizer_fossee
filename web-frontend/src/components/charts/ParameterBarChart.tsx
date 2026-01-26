import { Bar } from 'react-chartjs-2'

interface ParameterBarChartProps {
  avgFlowrate: number
  avgPressure: number
  avgTemperature: number
}

export default function ParameterBarChart({
  avgFlowrate,
  avgPressure,
  avgTemperature,
}: ParameterBarChartProps) {
  const data = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [avgFlowrate, avgPressure, avgTemperature],
        backgroundColor: [
          'rgba(59, 130, 246, 0.6)',
          'rgba(168, 85, 247, 0.6)',
          'rgba(249, 115, 22, 0.6)',
        ],
        borderColor: ['rgb(59, 130, 246)', 'rgb(168, 85, 247)', 'rgb(249, 115, 22)'],
        borderWidth: 2,
      },
    ],
  }

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
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
      <h3 className="text-lg font-semibold mb-6 text-white">Average Parameters</h3>
      <Bar data={data} options={options} />
    </div>
  )
}
