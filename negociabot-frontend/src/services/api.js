import axios from 'axios';

const API_URL = 'https://negociabot.onrender.com';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Intercepteur pour ajouter le token automatiquement
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ============ AUTH ============
export const login = (email, mot_de_passe) =>
  api.post('/auth/login', { email, mot_de_passe });

export const register = (data) =>
  api.post('/auth/register', data);

export const getProfil = () =>
  api.get('/auth/me');

// ============ COMMERCANTS ============
export const getCommercant = (commercant_id) =>
  api.get(`/commercants/${commercant_id}`);

// ============ PRODUITS ============
export const getProduits = (commercant_id) =>
  api.get(`/produits/${commercant_id}`);

export const creerProduit = (commercant_id, data) =>
  api.post(`/produits/${commercant_id}`, data);

export const supprimerProduit = (produit_id) =>
  api.delete(`/produits/supprimer/${produit_id}`);

export const modifierProduit = (produit_id, data) =>
  api.put(`/produits/modifier/${produit_id}`, data);

export const getProduitDetail = (produit_id) =>
  api.get(`/produits/detail/${produit_id}`);

// ============ NEGOCIATIONS ============
export const getNegociations = (commercant_id) =>
  api.get(`/negotiation/conversations/${commercant_id}`);

export const updateNegociation = (id, data) =>
  api.put(`/negotiation/conversations/${id}`, data);

export const envoyerMessage = (commercant_id, data) =>
  api.post(`/negotiation/message/${commercant_id}`, data);

export const getConversations = (commercant_id) =>
  api.get(`/negotiation/conversations/${commercant_id}`);

export const getHistorique = (conversation_id) =>
  api.get(`/negotiation/historique/${conversation_id}`);

// ============ DASHBOARD ============
export const getDashboard = (commercant_id) =>
  api.get(`/dashboard/${commercant_id}`);

// ============ ABONNEMENT ============
export const getPlansAbonnement = () =>
  api.get('/abonnements/plans');

export const getAbonnement = (commercant_id) =>
  api.get(`/abonnements/${commercant_id}`);

export const upgradeAbonnement = (commercant_id, data) =>
  api.post(`/abonnements/souscrire/${commercant_id}`, data);

// ============ PAIEMENT ============
export const initierMomo = (data) =>
  api.post('/paiement/momo/initier', data);

export const confirmerMomo = (data) =>
  api.post('/paiement/momo/confirmer', data);

export const initierOrange = (data) =>
  api.post('/paiement/orange/initier', data);

export const confirmerOrange = (data) =>
  api.post('/paiement/orange/confirmer', data);

export const getMethodesPaiement = () =>
  api.get('/paiement/methodes');

export const initierPaiement = (data) => {
  if (data.operateur === 'momo') {
    return initierMomo(data);
  } else {
    return initierOrange(data);
  }
};

export const verifierPaiement = (reference) =>
  api.get(`/paiement/verifier/${reference}`);

// ============ WHATSAPP ============
export const envoyerWhatsApp = (data) =>
  api.post('/whatsapp/envoyer', data);

export const getWhatsAppStatus = () =>
  api.get('/whatsapp/config');

export default api;