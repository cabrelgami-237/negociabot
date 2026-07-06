import React, { useState } from 'react';
import { register, login } from '../services/api';

export default function Inscription({ onLogin, onRetourLogin }) {
  const [nomBoutique, setNomBoutique] = useState('');
  const [email, setEmail] = useState('');
  const [telephone, setTelephone] = useState('');
  const [domaineActivite, setDomaineActivite] = useState('');
  const [motDePasse, setMotDePasse] = useState('');
  const [confirmation, setConfirmation] = useState('');
  const [erreur, setErreur] = useState('');
  const [chargement, setChargement] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErreur('');

    if (motDePasse !== confirmation) {
      setErreur('Les mots de passe ne correspondent pas');
      return;
    }
    if (motDePasse.length < 6) {
      setErreur('Le mot de passe doit contenir au moins 6 caracteres');
      return;
    }

    setChargement(true);
    try {
      await register({
        nom_boutique: nomBoutique,
        email: email,
        telephone: telephone,
        mot_de_passe: motDePasse,
        domaine_activite: domaineActivite,
      });

      // Connexion automatique apres inscription reussie
      const res = await login(email, motDePasse);
      const data = res.data;
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('commercant_id', data.commercant_id);
      localStorage.setItem('nom_boutique', data.nom_boutique);
      onLogin(data);
    } catch (err) {
      setErreur(err.response?.data?.detail || "Erreur lors de l'inscription");
    }
    setChargement(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.logo}>🤝 NégociaBot</h1>
        <p style={styles.sousTitre}>Créez votre compte commerçant</p>

        <form onSubmit={handleSubmit}>
          <div style={styles.champ}>
            <label style={styles.label}>Nom de la boutique</label>
            <input
              style={styles.input}
              type="text"
              value={nomBoutique}
              onChange={(e) => setNomBoutique(e.target.value)}
              placeholder="Ex : Boutique Wax Douala"
              required
            />
          </div>

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
            <label style={styles.label}>Téléphone WhatsApp</label>
            <input
              style={styles.input}
              type="tel"
              value={telephone}
              onChange={(e) => setTelephone(e.target.value)}
              placeholder="Ex : 690123456"
              required
            />
          </div>

          <div style={styles.champ}>
            <label style={styles.label}>Domaine d'activité</label>
            <input
              style={styles.input}
              type="text"
              value={domaineActivite}
              onChange={(e) => setDomaineActivite(e.target.value)}
              placeholder="Ex : Vêtements, Électronique..."
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

          <div style={styles.champ}>
            <label style={styles.label}>Confirmer le mot de passe</label>
            <input
              style={styles.input}
              type="password"
              value={confirmation}
              onChange={(e) => setConfirmation(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          {erreur && <p style={styles.erreur}>{String(erreur)}</p>}

          <button style={styles.bouton} type="submit" disabled={chargement}>
            {chargement ? 'Création du compte...' : "S'inscrire"}
          </button>
        </form>

        <p style={styles.lien}>
          Déjà un compte ?{' '}
          <span style={styles.lienTexte} onClick={onRetourLogin}>
            Se connecter
          </span>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px 0',
  },
  card: {
    background: 'white',
    borderRadius: '16px',
    padding: '40px',
    width: '380px',
    boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
  },
  logo: {
    textAlign: 'center',
    fontSize: '28px',
    color: '#0f3460',
    marginBottom: '8px',
  },
  sousTitre: {
    textAlign: 'center',
    color: '#666',
    fontSize: '14px',
    marginBottom: '30px',
  },
  champ: { marginBottom: '20px' },
  label: { display: 'block', marginBottom: '6px', fontWeight: '600', color: '#333' },
  input: {
    width: '100%',
    padding: '12px',
    border: '2px solid #e0e0e0',
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
    width: '100%',
    padding: '14px',
    background: 'linear-gradient(135deg, #0f3460, #e94560)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '700',
    cursor: 'pointer',
  },
  lien: {
    textAlign: 'center',
    marginTop: '20px',
    fontSize: '14px',
    color: '#666',
  },
  lienTexte: {
    color: '#e94560',
    fontWeight: '700',
    cursor: 'pointer',
    textDecoration: 'underline',
  },
};