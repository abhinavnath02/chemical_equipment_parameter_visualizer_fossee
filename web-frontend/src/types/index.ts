export interface AnalysisResult {
  total_equipment: number
  avg_flowrate: number
  avg_pressure: number
  avg_temperature: number
  equipment_by_type?: { [key: string]: number }
  equipment_data?: Array<{
    name: string
    type: string
    flowrate: number
    pressure: number
    temperature: number
  }>
}

export interface HistoryItem {
  id: number
  filename: string
  uploaded_at: string
  total_equipment: number
}
