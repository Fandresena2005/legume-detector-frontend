// Centralise l'URL du backend ici. En local ça pointe vers FastAPI,
// en production remplace par l'URL de déploiement (ex: Render/Railway)
// via une variable d'environnement Vite (.env -> VITE_API_URL).
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
