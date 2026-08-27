export interface PredictionResult {
  status: 'success'
  prediction: string
  confidence: number
  probabilities?: Record<string, number> | null
}

export interface PredictionState {
  result: PredictionResult | null
  loading: boolean
  error: string | null
}
