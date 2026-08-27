export interface PredictionResult {
  classe: string
  confiance: number
}

export interface PredictionState {
  result: PredictionResult | null
  loading: boolean
  error: string | null
}
