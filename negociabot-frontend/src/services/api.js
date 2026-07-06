import axios from 'axios';

const API_URL = 'https://negociabot.onrender.com';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
});

// Ajouter le token automatiquement
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auth
export const login = (email, mot_de_passe) =>
  api.post('/auth/login', { email, mot_de_passe });

export const register = (data) =>
  api.post('/commercants/register', data);

// Produits
export const getProduits = (commercant_id) =>
  api.get(`/produits/${commercant_id}`);

export const creerProduit = (commercant_id, data) =>
  api.post(`/produits/${commercant_id}`, data);

export const supprimerProduit = (produit_id) =>
  api.delete(`/produits/supprimer/${produit_id}`);

// Négociation
export const envoyerMessage = (commercant_id, data) =>
  api.post(`/negotiation/message/${commercant_id}`, data);

export const getConversations = (commercant_id) =>
  api.get(`/negotiation/conversations/${commercant_id}`);

export const getHistorique = (conversation_id) =>
  api.get(`/negotiation/historique/${conversation_id}`);

// Dashboard
export const getDashboard = (commercant_id) =>
  api.get(`/dashboard/${commercant_id}`);

// Paiement MTN MoMo
export const initierMomo = (data) =>
  api.post('/paiement/momo/initier', data);

export const confirmerMomo = (data) =>
  api.post('/paiement/momo/confirmer', data);

// Paiement Orange Money
export const initierOrange = (data) =>
  api.post('/paiement/orange/initier', data);

export const confirmerOrange = (data) =>
  api.post('/paiement/orange/confirmer', data);

// Méthodes disponibles
export const getMethodesPaiement = () =>
  api.get('/paiement/methodes');