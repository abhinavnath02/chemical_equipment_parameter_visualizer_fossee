import { useEffect, useRef } from 'react'
import { Chart, TooltipItem } from 'chart.js'

interface SafetyStatusChartProps {
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

export default function SafetyStatusChart({ equipmentData, thresholds = DEFAULT_THRESHOLDS }: SafetyStatusChartProps) {
  const chartRef = useRef<HTMLCanvasElement>(null)
  const chartInstance = useRef<Chart | null>(null)

  useEffect(() => {
    if (!chartRef.current) return

    const categorizeValues = (values: number[], param: keyof typeof thresholds) => {
      const safe = values.filter(v => v >= thresholds[param].min && v <= thresholds[param].max).length
      const warning = values.filter(v => 
        (v > thresholds[param].max && v <= thresholds[param].critical_max) || v < thresholds[param].min
      ).length
      const critical = values.filter(v => v > thresholds[param].critical_max).length
      return { safe, warning, critical }
    }

    const flowrates = equipmentData.map(e => e.flowrate)
    const pressures = equipmentData.map(e => e.pressure)
    const temperatures = equipmentData.map(e => e.temperature)

    const flowStatus = categorizeValues(flowrates, 'flowrate')
    const pressStatus = categorizeValues(pressures, 'pressure')
    const tempStatus = categorizeValues(temperatures, 'temperature')

    const config: any = {
      type: 'bar',
      data: {
        labels: ['Flowrate', 'Pressure', 'Temperature'],
        datasets: [
          {
            label: 'Safe',
            data: [flowStatus.safe, pressStatus.safe, tempStatus.safe],
            backgroundColor: '#22c55e',
            borderColor: '#16a34a',
            borderWidth: 2
          },
          {
            label: 'Warning',
            data: [flowStatus.warning, pressStatus.warning, tempStatus.warning],
            backgroundColor: '#f59e0b',
            borderColor: '#d97706',
            borderWidth: 2
          },
          {
            label: 'Critical',
            data: [flowStatus.critical, pressStatus.critical, tempStatus.critical],
            backgroundColor: '#ef4444',
            borderColor: '#dc2626',
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: '#d1d5db',
              font: { size: 12, weight: 'bold' }
            }
          },
          title: {
            display: true,
            text: 'Equipment Safety Status Distribution',
            color: '#ffffff',
            font: { size: 16, weight: 'bold' }
          },
          tooltip: {
            callbacks: {
              label: (context: TooltipItem<'bar'>) => {
                return `${context.dataset.label}: ${context.parsed.y} equipment`
              }
            }
          }
        },
        scales: {
          x: {
            stacked: true,
            grid: { color: '#3f3f46', display: false },
            ticks: { color: '#d1d5db', font: { size: 11 } }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            grid: { color: '#3f3f46' },
            ticks: { 
              color: '#d1d5db',
              font: { size: 11 },
              stepSize: 1
            },
            title: {
              display: true,
              text: 'Equipment Count',
              color: '#d1d5db'
            }
          }
        }
      }
    }

    if (chartInstance.current) {
      chartInstance.current.destroy()
    }

    chartInstance.current = new Chart(chartRef.current, config)

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy()
      }
    }
  }, [equipmentData, thresholds])

  return <canvas ref={chartRef} />
}
