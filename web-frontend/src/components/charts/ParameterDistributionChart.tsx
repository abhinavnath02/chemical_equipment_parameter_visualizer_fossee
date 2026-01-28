import { useEffect, useRef } from 'react'
import { Chart } from 'chart.js'

interface ParameterDistributionChartProps {
  equipmentData: Array<{
    name: string
    type: string
    flowrate: number
    pressure: number
    temperature: number
  }>
  parameter: 'flowrate' | 'pressure' | 'temperature'
}

export default function ParameterDistributionChart({ equipmentData, parameter }: ParameterDistributionChartProps) {
  const chartRef = useRef<HTMLCanvasElement>(null)
  const chartInstance = useRef<Chart | null>(null)

  useEffect(() => {
    if (!chartRef.current) return

    const values = equipmentData.map(e => e[parameter])
    const min = Math.min(...values)
    const max = Math.max(...values)
    const range = max - min
    const binCount = 10
    const binSize = range / binCount

    const bins = Array(binCount).fill(0)
    const binLabels = []

    for (let i = 0; i < binCount; i++) {
      const binStart = min + (i * binSize)
      const binEnd = binStart + binSize
      binLabels.push(`${binStart.toFixed(0)}-${binEnd.toFixed(0)}`)
      
      values.forEach(v => {
        if (v >= binStart && (v < binEnd || (i === binCount - 1 && v === binEnd))) {
          bins[i]++
        }
      })
    }

    const colors = {
      flowrate: { bg: '#ef444480', border: '#ef4444' },
      pressure: { bg: '#3b82f680', border: '#3b82f6' },
      temperature: { bg: '#22c55e80', border: '#22c55e' }
    }

    const titles = {
      flowrate: 'Flowrate Distribution',
      pressure: 'Pressure Distribution',
      temperature: 'Temperature Distribution'
    }

    const config: any = {
      type: 'bar',
      data: {
        labels: binLabels,
        datasets: [{
          label: `${parameter.charAt(0).toUpperCase() + parameter.slice(1)} Count`,
          data: bins,
          backgroundColor: colors[parameter].bg,
          borderColor: colors[parameter].border,
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          title: {
            display: true,
            text: titles[parameter],
            color: '#ffffff',
            font: { size: 14, weight: 'bold' }
          },
          tooltip: {
            callbacks: {
              label: (context) => `${context.parsed.y} equipment`
            }
          }
        },
        scales: {
          x: {
            grid: { color: '#3f3f46', display: false },
            ticks: { 
              color: '#d1d5db',
              font: { size: 9 },
              maxRotation: 45,
              minRotation: 45
            }
          },
          y: {
            beginAtZero: true,
            grid: { color: '#3f3f46' },
            ticks: { 
              color: '#d1d5db',
              font: { size: 10 },
              stepSize: 1
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
  }, [equipmentData, parameter])

  return <canvas ref={chartRef} />
}
