<script setup lang="ts">
import ImageUploader from "@/components/ImageUploader.vue";
import PredictionResult from "@/components/PredictionResult.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import { usePrediction } from "@/composables/usePrediction";

const { predict, result, loading, error } = usePrediction();

const caracteristiques = [
  {
    title: "Analyse instantanée",
    text: "Détection rapide de la qualité visuelle d’un fruit ou d’un légume à partir d’une simple photo.",
    icon: "bolt",
  },
  {
    title: "Décisions fiables",
    text: "Un score de confiance pour aider à trier, vendre ou consommer avec plus de sécurité.",
    icon: "check",
  },
  {
    title: "Gaspillage réduit",
    text: "Identifiez les aliments encore consommables et évitez les déchets inutiles.",
    icon: "leaf",
  },
];

const etapes = [
  {
    number: "01",
    title: "Téléchargez une photo",
    text: "Prenez une image nette d’un fruit ou d’un légume, posé sur une surface claire.",
  },
  {
    number: "02",
    title: "L’IA analyse les détails",
    text: "Le modèle repère les signes de fraîcheur, moisissure ou dégradation.",
  },
  {
    number: "03",
    title: "Recevez un verdict clair",
    text: "Obtenez un résultat précis avec un niveau de confiance affiché.",
  },
];

const statistiques = [
  { value: "96%", label: "Précision visuelle" },
  { value: "3x", label: "Plus rapide qu’un contrôle manuel" },
  { value: "24/7", label: "Disponibilité et simplicité" },
];
</script>

<template>
  <div class="page-shell text-stone-800">
    <a
      href="#contenu-principal"
      class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-stone-900 focus:px-4 focus:py-3 focus:text-sm focus:font-semibold focus:text-white"
    >
      Aller au contenu principal
    </a>
    <header
      class="sticky top-0 z-30 border-b border-stone-200/80 bg-[#f6f4ed]/85 backdrop-blur-xl"
    >
      <div
        class="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-8"
      >
        <a href="#contenu-principal" class="flex items-center gap-3" aria-label="Fruit & Légumes Detector, accueil">
          <div
            class="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#147d5a] text-lg font-bold text-white shadow-lg shadow-emerald-900/15"
          >
            V
          </div>
          <div>
            <p class="text-base font-bold text-stone-900">
              Fruit &amp; Légumes Detector
            </p>
          </div>
        </a>

        <nav
          class="hidden items-center gap-8 text-sm font-medium text-stone-600 md:flex"
          aria-label="Navigation principale"
        >
          <a href="#fonctionnement" class="transition hover:text-stone-900"
            >Fonctionnement</a
          >
          <a href="#avantages" class="transition hover:text-stone-900"
            >Avantages</a
          >
          <a href="#demo" class="transition hover:text-stone-900">Démo</a>
        </nav>

        <a
          href="#demo"
          class="rounded-full bg-stone-900 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-stone-200 transition hover:-translate-y-0.5 hover:bg-stone-800"
        >
          Tester maintenant
        </a>
      </div>
    </header>

    <main id="contenu-principal">
      <section class="relative overflow-hidden">
        <div class="absolute inset-0 bg-[#e8f0e5]/75" />

        <div
          class="relative mx-auto grid max-w-7xl items-center gap-12 px-6 py-20 lg:grid-cols-[1.15fr_0.85fr] lg:px-8 lg:py-28"
        >
          <div>
            <div
              class="mb-6 inline-flex items-center gap-2 rounded-full border border-[#f2c8a5] bg-[#fff4e9] px-4 py-2 text-sm font-medium text-[#a45327]"
            >
              <svg
                viewBox="0 0 24 24"
                class="h-4 w-4 text-[#df8248]"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path d="M12 2v7M9 5h6M7 12h10M12 12v10" />
              </svg>
              IA pour réduire le gaspillage alimentaire
            </div>

            <h1
              class="max-w-xl text-4xl font-black tracking-tight text-stone-900 sm:text-5xl lg:text-6xl"
            >
              Détectez la fraîcheur des fruits et légumes en quelques secondes.
            </h1>

            <p class="mt-6 max-w-xl text-lg leading-8 text-stone-600">
              Une solution intelligente pour vérifier rapidement si un fruit ou
              un légume est sain, encore consommable ou à jeter, grâce à une
              analyse visuelle assistée par intelligence artificielle.
            </p>

            <div class="mt-8 flex flex-wrap gap-4">
              <a
                href="#demo"
                class="rounded-full bg-[#df8248] px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-orange-900/15 transition hover:-translate-y-0.5 hover:bg-[#c96f38]"
              >
                Essayer le détecteur
              </a>
              <a
                href="#fonctionnement"
                class="rounded-full border border-stone-200 bg-white/80 px-6 py-3.5 text-sm font-semibold text-stone-700 transition hover:border-stone-300 hover:bg-white"
              >
                Voir le fonctionnement
              </a>
            </div>

            <div class="mt-10 grid max-w-lg grid-cols-3 gap-4">
              <div
                v-for="statistique in statistiques"
                :key="statistique.label"
                class="rounded-2xl border border-stone-200 bg-white/70 p-4 shadow-sm backdrop-blur-sm"
              >
                <p class="text-2xl font-black text-stone-900">
                  {{ statistique.value }}
                </p>
                <p class="mt-1 text-xs leading-5 text-stone-600">
                  {{ statistique.label }}
                </p>
              </div>
            </div>
          </div>

          <div class="relative">
            <div
              class="relative overflow-hidden rounded-[2rem] border border-lime-100 bg-white p-4 shadow-[0_30px_80px_rgba(15,23,42,0.08)]"
            >
              <div class="rounded-[1.5rem] bg-lime-50 p-5">
                <div
                  class="rounded-[1.25rem] bg-white p-4 shadow-sm ring-1 ring-stone-100"
                >
                  <div class="mb-4 flex items-center justify-between">
                    <div>
                      <p
                        class="text-xs font-semibold uppercase tracking-[0.2em] text-lime-700"
                      >
                        Analyse
                      </p>
                      <h2 class="mt-1 text-xl font-bold text-stone-900">
                        Fruit détecté
                      </h2>
                    </div>
                    <span
                      class="rounded-full bg-lime-100 px-2.5 py-1 text-xs font-bold text-lime-700"
                      >Sain</span
                    >
                  </div>

                  <div class="rounded-[1.25rem] bg-emerald-50 p-3">
                    <div
                      class="flex items-center justify-center rounded-[1rem] border border-dashed border-lime-200 bg-white/80 p-8"
                    >
                      <div
                        class="flex h-28 w-28 items-center justify-center rounded-full bg-emerald-500 shadow-lg shadow-lime-200"
                      >
                        <svg
                          viewBox="0 0 64 64"
                          class="h-16 w-16 text-white"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2.5"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          aria-hidden="true"
                        >
                          <path
                            d="M28 18c-5 2-9 7-10 13-1 8 3 17 11 22 8-5 12-14 11-22-1-6-5-11-12-13Z"
                          />
                          <path
                            d="M31 18c0-6 5-11 11-11 5 0 9 3 10 8-4 2-8 5-10 9-2-2-7-4-11-6Z"
                          />
                          <path
                            d="M20 27c-7 2-12 8-12 15 0 9 8 17 18 17 5 0 9-2 12-5"
                          />
                          <path d="M31 30c3 2 6 5 8 9" />
                          <path d="M25 38c3 1 6 1 9-1" />
                        </svg>
                      </div>
                    </div>
                  </div>

                  <div class="mt-5 space-y-3">
                    <div
                      class="flex items-center justify-between text-sm text-stone-600"
                    >
                      <span>Confiance</span>
                      <span class="font-semibold text-stone-900">94%</span>
                    </div>
                    <div
                      class="h-2.5 w-full overflow-hidden rounded-full bg-stone-100"
                    >
                      <div class="h-full w-[94%] rounded-full bg-emerald-500" />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div
              class="absolute -bottom-6 -left-3 rounded-2xl border border-emerald-200 bg-white px-4 py-3 shadow-xl shadow-emerald-100"
            >
              <p class="text-xs uppercase tracking-[0.2em] text-stone-500">
                Réduction
              </p>
              <p class="mt-1 text-2xl font-black text-stone-900">-32%</p>
              <p class="text-xs text-stone-600">de gaspillage alimentaire</p>
            </div>
          </div>
        </div>
      </section>

      <section id="avantages" aria-labelledby="avantages-titre" class="mx-auto max-w-7xl scroll-mt-24 px-6 py-20 lg:px-8">
        <div class="mx-auto max-w-2xl text-center">
          <p
            class="text-sm font-semibold uppercase tracking-[0.2em] text-lime-700"
          >
            Pourquoi c’est utile
          </p>
          <h2 id="avantages-titre" class="mt-4 text-3xl font-black text-stone-900 sm:text-4xl">
            Un outil pensé pour agir plus vite et mieux.
          </h2>
        </div>

        <div class="mt-12 grid gap-6 md:grid-cols-3">
          <article
            v-for="caracteristique in caracteristiques"
            :key="caracteristique.title"
            class="rounded-[1.75rem] border border-stone-200 bg-white p-7 shadow-sm transition hover:-translate-y-1 hover:shadow-xl hover:shadow-stone-100"
          >
            <div
              class="flex h-14 w-14 items-center justify-center rounded-2xl bg-lime-100 shadow-inner shadow-lime-200"
            >
              <svg
                v-if="caracteristique.icon === 'bolt'"
                viewBox="0 0 24 24"
                class="h-7 w-7 text-lime-700"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path d="M13 2 4 13h6l-1 9 9-11h-6l1-9Z" />
              </svg>
              <svg
                v-else-if="caracteristique.icon === 'check'"
                viewBox="0 0 24 24"
                class="h-7 w-7 text-lime-700"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path d="M20 6 9 17l-5-5" />
              </svg>
              <svg
                v-else
                viewBox="0 0 24 24"
                class="h-7 w-7 text-lime-700"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path
                  d="M12 3c2.8 2.6 4 5.3 4 8.3A4 4 0 0 1 8 11.3C8 8.3 9.2 5.6 12 3Z"
                />
                <path d="M12 13c0 3 3 5 6 5" />
                <path d="M12 13c0 3-3 5-6 5" />
              </svg>
            </div>
            <h3 class="mt-6 text-xl font-bold text-stone-900">
              {{ caracteristique.title }}
            </h3>
            <p class="mt-3 text-base leading-7 text-stone-600">
              {{ caracteristique.text }}
            </p>
          </article>
        </div>
      </section>

      <section id="fonctionnement" aria-labelledby="fonctionnement-titre" class="scroll-mt-24 bg-stone-950 py-20 text-white">
        <div class="mx-auto max-w-7xl px-6 lg:px-8">
          <div class="mx-auto max-w-2xl text-center">
            <p
              class="text-sm font-semibold uppercase tracking-[0.2em] text-lime-300"
            >
              Comment ça marche
            </p>
            <h2 id="fonctionnement-titre" class="mt-4 text-3xl font-black sm:text-4xl">
              Une expérience simple, claire et immédiate.
            </h2>
          </div>

          <div class="mt-12 grid gap-6 md:grid-cols-3">
            <div
              v-for="etape in etapes"
              :key="etape.number"
              class="rounded-[1.75rem] border border-white/10 bg-white/5 p-7 backdrop-blur-sm"
            >
              <p
                class="text-sm font-semibold uppercase tracking-[0.2em] text-lime-300"
              >
                {{ etape.number }}
              </p>
              <h3 class="mt-5 text-2xl font-bold">{{ etape.title }}</h3>
              <p class="mt-3 text-base leading-7 text-stone-300">
                {{ etape.text }}
              </p>
            </div>
          </div>
        </div>
      </section>

      <section id="demo" aria-labelledby="demo-titre" class="mx-auto max-w-7xl scroll-mt-24 px-6 py-20 lg:px-8">
        <div class="mb-10 text-center">
          <p
            class="text-sm font-semibold uppercase tracking-[0.2em] text-lime-700"
          >
            Démo produit
          </p>
          <h2 id="demo-titre" class="mt-4 text-3xl font-black text-stone-900 sm:text-4xl">
            Testez directement l’outil
          </h2>
        </div>

        <div
          class="mx-auto max-w-4xl rounded-[2rem] border border-stone-200 bg-white p-5 shadow-[0_25px_60px_rgba(15,23,42,0.08)] md:p-8"
        >
          <div class="grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
            <div class="rounded-[1.5rem] bg-stone-50 p-5 ring-1 ring-stone-200">
              <p
                class="text-sm font-semibold uppercase tracking-[0.2em] text-stone-500"
              >
                Uploader
              </p>
              <div class="mt-4">
                <ImageUploader @file-selected="predict" />
              </div>
            </div>

              <div class="flex flex-col justify-center" aria-live="polite" aria-atomic="true">
              <div class="space-y-4">
                <LoadingSpinner v-if="loading" />
                <p
                  v-if="error"
                  class="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-600"
                >
                  {{ error }}
                </p>
                <PredictionResult v-if="result" :result="result" />
              </div>

              <div
                v-if="!result"
                class="mt-6 rounded-[1.5rem] border border-dashed border-stone-300 bg-stone-50 p-6 text-stone-600"
              >
                <p class="text-lg font-semibold text-stone-800">
                  Prêt à analyser un fruit ou un légume ?
                </p>
                <p class="mt-2 text-sm leading-6">
                  Ajoutez une photo pour visualiser le verdict du modèle, son
                  niveau de confiance et la classification détectée.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="mx-auto max-w-7xl px-6 pb-20 lg:px-8">
        <div
          class="overflow-hidden rounded-[2rem] border border-emerald-500 bg-emerald-500 p-px shadow-[0_30px_80px_rgba(16,185,129,0.25)]"
        >
          <div
            class="rounded-[calc(2rem-1px)] bg-white px-6 py-10 text-center md:px-10"
          >
            <p
              class="text-sm font-semibold uppercase tracking-[0.2em] text-lime-700"
            >
              Pour qui ?
            </p>
            <h2 class="mt-4 text-3xl font-black text-stone-900">
              Une solution utile pour les particuliers, commerçants et
              agriculteurs.
            </h2>
            <p
              class="mx-auto mt-4 max-w-2xl text-base leading-7 text-stone-600"
            >
              Que vous gériez un panier de fruits et légumes, une petite
              boutique ou une production locale, l’outil vous aide à prendre des
              décisions plus intelligentes et moins de gaspillage.
            </p>
          </div>
        </div>
      </section>
    </main>

    <footer class="border-t border-stone-200 bg-stone-50">
      <div
        class="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-6 py-8 text-sm text-stone-600 md:flex-row lg:px-8"
      >
        <p class="font-medium text-stone-700">
          VeggieVision — Détection intelligente de la fraîcheur alimentaire
        </p>
        <p>© 2026 • IA pour un meilleur usage des légumes</p>
      </div>
    </footer>
  </div>
</template>
