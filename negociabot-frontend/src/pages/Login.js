import React, { useState } from 'react';
import { login } from '../services/api';
import logo from '../assets/logo-negociabot.jpeg';

export default function Login({ onLogin, onInscription }) {
  const [email, setEmail] = useState('');
  const [motDePasse, setMotDePasse] = useState('');
  const [erreur, setErreur] = useState('');
  const [chargement, setChargement] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setChargement(true);
    setErreur('');
    try {
      const res = await login(email, motDePasse);
      const data = res.data;
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('commercant_id', data.commercant_id);
      localStorage.setItem('nom_boutique', data.nom_boutique);
      onLogin(data);
    } catch (err) {
      setErreur(err.response?.data?.detail || 'Erreur de connexion');
    }
    setChargement(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <img src={logo} alt="NégociaBot" style={styles.logoImg} />
        <p style={styles.sousTitre}>Système de négociation IA — Cameroun</p>
        <form onSubmit={handleSubmit}>
          <div style={styles.champ}>
            <label style={styles.label}>Email</label>
            <input
              style={styles.input}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="votre@email.com"
              required
            />
          </div>
          <div style={styles.champ}>
            <label style={styles.label}>Mot de passe</label>
            <input
              style={styles.input}
              type="password"
              value={motDePasse}
              onChange={(e) => setMotDePasse(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
          {erreur && <p style={styles.erreur}>{String(erreur)}</p>}
          <button className="btn btn-block" style={styles.bouton} type="submit" disabled={chargement}>
            {chargement ? 'Connexion...' : 'Se connecter'}
          </button>
        </form>
        <p style={styles.lien}>
          Pas encore de compte ?{' '}
          <span style={styles.lienTexte} onClick={onInscription}>
            Créer un compte
          </span>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #0A3D62 0%, #0f2942 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
  },
  card: {
    background: 'white',
    borderRadius: '16px',
    padding: '40px',
    width: '380px',
    maxWidth: '100%',
    boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
  },
  logoImg: {
    display: 'block',
    margin: '0 auto 12px',
    width: '160px',
    height: 'auto',
  },
  sousTitre: {
    textAlign: 'center',
    color: '#64748B',
    fontSize: '14px',
    marginBottom: '30px',
  },
  champ: { marginBottom: '20px' },
  label: { display: 'block', marginBottom: '6px', fontWeight: '600', color: '#1E293B' },
  input: {
    width: '100%',
    padding: '12px',
    border: '2px solid #E2E8F0',
    borderRadius: '8px',
    fontSize: '15px',
    boxSizing: 'border-box',
    outline: 'none',
  },
  erreur: {
    color: '#e74c3c',
    background: '#ffeaea',
    padding: '10px',
    borderRadius: '8px',
    fontSize: '14px',
    marginBottom: '15px',
  },
  bouton: {
    background: '#1A73E8',
    color: 'white',
    fontSize: '16px',
  },
  lien: {
    textAlign: 'center',
    marginTop: '20px',
    fontSize: '14px',
    color: '#64748B',
  },
  lienTexte: {
    color: '#1A73E8',
    fontWeight: '700',
    cursor: 'pointer',
    textDecoration: 'underline',
  },
};