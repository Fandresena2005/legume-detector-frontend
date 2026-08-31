<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  fileSelected: [file: File]
}>()

const previewUrl = ref<string | null>(null)
const isDragging = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

function handleFile(file: File) {
  if (!file.type.startsWith('image/')) return
  previewUrl.value = URL.createObjectURL(file)
  emit('fileSelected', file)
}

function onDrop(e: DragEvent) {
  e.preventDefault()
  isDragging.value = false
  const file = e.dataTransfer?.files[0]
  if (file) handleFile(file)
}

function onFileInputChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) handleFile(file)
}

function openFilePicker() {
  fileInput.value?.click()
}

defineExpose({ previewUrl })
</script>

<template>
  <div
    role="button"
    tabindex="0"
    aria-label="Déposer une photo d’un fruit ou d’un légume"
    @click="openFilePicker"
    @keydown.enter="openFilePicker"
    @keydown.space.prevent="openFilePicker"
    @drop="onDrop"
    @dragover.prevent="isDragging = true"
    @dragleave="isDragging = false"
    class="group relative overflow-hidden rounded-3xl border-2 border-dashed p-8 text-center transition-all cursor-pointer focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-500 sm:p-10"
    :class="isDragging
      ? 'border-lime-500 bg-lime-50'
      : 'border-stone-300 hover:border-emerald-400 hover:bg-[#f4f8f1]'"
  >
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      class="hidden"
      @change="onFileInputChange"
    />

    <div v-if="!previewUrl" class="flex flex-col items-center gap-3">
      <div class="flex h-14 w-14 items-center justify-center rounded-full bg-lime-100 text-lime-700">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 16V4m0 0L7 9m5-5 5 5M5 20h14" />
        </svg>
      </div>
      <p class="font-medium text-stone-700">Dépose une photo d’un fruit ou d’un légume ici</p>
      <p class="text-sm text-stone-400">ou clique pour en choisir une · JPG, PNG</p>
    </div>

    <div v-else class="mx-auto max-w-xs">
      <img :src="previewUrl" alt="Aperçu de l'image sélectionnée" class="rounded-2xl shadow-md" />
      <p class="mt-3 text-sm font-medium text-stone-500">Clique pour changer de photo</p>
    </div>
  </div>
</template>
