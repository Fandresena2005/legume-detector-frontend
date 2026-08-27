import { ref } from 'vue'
import type { PredictionResult } from '@/types/prediction'
import { API_URL } from '@/config'

export function usePrediction() {
  const result = ref<PredictionResult | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function predict(file: File) {
    loading.value = true
    error.value = null
    result.value = null

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Erreur serveur (${response.status})`)
      }

      result.value = (await response.json()) as PredictionResult
    } catch (e) {
      error.value =
        e instanceof Error
          ? e.message
          : "Impossible d'analyser cette image. Vérifie que le backend tourne."
    } finally {
      loading.value = false
    }
  }

  function reset() {
    result.value = null
    error.value = null
    loading.value = false
  }

  return { predict, reset, result, loading, error }
}
