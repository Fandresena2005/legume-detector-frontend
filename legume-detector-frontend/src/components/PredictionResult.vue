<script setup lang="ts">
import { computed } from 'vue'
import type { PredictionResult } from '@/types/prediction'

const props = defineProps<{
  result: PredictionResult
}>()

const isRotten = computed(() => props.result.classe.toLowerCase().includes('rotten'))
const confidencePct = computed(() => Math.round(props.result.confiance * 100))

const label = computed(() =>
  props.result.classe
    .replace(/_/g, ' ')
    .replace('Healthy', '— Sain')
    .replace('Rotten', '— Pourri')
)
</script>

<template>
  <div
    class="rounded-3xl border p-6 transition-colors"
    :class="isRotten ? 'border-rose-200 bg-rose-50' : 'border-lime-200 bg-lime-50'"
  >
    <div class="flex items-center gap-3">
      <span
        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-lg"
        :class="isRotten ? 'bg-rose-500 text-white' : 'bg-lime-600 text-white'"
      >
        {{ isRotten ? '✕' : '✓' }}
      </span>
      <div>
        <p class="font-semibold text-stone-800">{{ label }}</p>
        <p class="text-sm text-stone-500">Confiance du modèle : {{ confidencePct }}%</p>
      </div>
    </div>

    <div class="mt-4 h-2 w-full overflow-hidden rounded-full bg-stone-200">
      <div
        class="h-full rounded-full transition-all duration-700 ease-out"
        :class="isRotten ? 'bg-rose-500' : 'bg-lime-600'"
        :style="{ width: confidencePct + '%' }"
      />
    </div>
  </div>
</template>
