<script setup lang="ts">
import ImageUploader from '@/components/ImageUploader.vue'
import PredictionResult from '@/components/PredictionResult.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { usePrediction } from '@/composables/usePrediction'

const { predict, result, loading, error } = usePrediction()
</script>

<template>
  <div class="min-h-screen bg-stone-50 text-stone-800">
    <div class="mx-auto max-w-xl px-6 py-16">
      <header class="mb-10 text-center">
        <p class="text-sm font-medium uppercase tracking-widest text-lime-600">Détecteur de fraîcheur</p>
        <h1 class="mt-2 text-3xl font-bold text-stone-900">Ce légume est-il encore bon ?</h1>
        <p class="mt-3 text-stone-500">
          Prends une photo, l'IA te dit s'il est sain ou en train de pourrir.
        </p>
      </header>

      <ImageUploader @file-selected="predict" />

      <div class="mt-6 space-y-4">
        <LoadingSpinner v-if="loading" />
        <p v-if="error" class="rounded-xl bg-rose-50 px-4 py-3 text-sm text-rose-600">
          {{ error }}
        </p>
        <PredictionResult v-if="result" :result="result" />
      </div>

      <footer class="mt-16 text-center text-xs text-stone-400">
        Projet IA — Détection de fraîcheur des fruits &amp; légumes
      </footer>
    </div>
  </div>
</template>
