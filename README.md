# Détecteur de fraîcheur — Frontend

Interface Vue 3 + TypeScript + Tailwind pour le projet IA de détection de fruits/légumes sains ou pourris. Le frontend envoie une photo au backend FastAPI (route `/predict`) et affiche le résultat.

## Stack

- Vue 3 (Composition API)
- TypeScript
- Vite
- Tailwind CSS v4

## Démarrer en local

```bash
npm install
cp .env.example .env   # adapte VITE_API_URL si besoin
npm run dev
```

Le site tourne sur `http://localhost:5173`. Assure-toi que le backend FastAPI tourne en parallèle (par défaut sur `http://localhost:8000`).

## Structure du projet

```
src/
├── components/
│   ├── ImageUploader.vue      # drag & drop + preview de la photo
│   ├── PredictionResult.vue   # affichage du résultat (classe + % confiance)
│   └── LoadingSpinner.vue     # état de chargement pendant l'appel API
├── composables/
│   └── usePrediction.ts       # logique d'appel à l'API /predict
├── types/
│   └── prediction.ts          # interfaces TypeScript des réponses API
├── config.ts                  # URL du backend (via variable d'env)
├── App.vue                    # page principale
└── main.ts
```

## Workflow Git pour l'équipe

1. Ne travaille jamais directement sur `main`
2. Crée une branche par tâche :
   ```bash
   git checkout -b feature/nom-de-la-tache
   ```
3. Commit régulièrement avec des messages clairs
4. Pousse ta branche et ouvre une Pull Request sur GitHub :
   ```bash
   git push origin feature/nom-de-la-tache
   ```
5. Fais relire par au moins un autre membre avant de merger dans `main`

## À faire / pistes d'amélioration

- [ ] Brancher l'URL du backend une fois déployé (Render/Railway)
- [ ] Ajouter un historique des dernières prédictions (Pinia si besoin)
- [ ] Gérer le cas d'erreur réseau plus finement
- [ ] Ajouter des tests sur `usePrediction`
