import React, { useState, useEffect } from 'react';
import { getDashboard } from '../services/api';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [chargement, setChargement] = useState(true);
  const commercant_id = localStorage.getItem('commercant_id');
  const nom_boutique = localStorage.getItem('nom_boutique');

  useEffect(() => {
    getDashboard(commercant_id)
      .then(res => { setData(res.data); setChargement(false); })
      .catch(() => setChargement(false));
  }, [commercant_id]);

  if (chargement) return <p style={styles.chargement}>Chargement...</p>;
  if (!data) return <p style={styles.chargement}>Erreur de chargement</p>;

  return (
    <div style={styles.container}>
      <h2 style={styles.titre}>Bonjour, {nom_boutique} 👋</h2>
      <p style={styles.sousTitre}>Voici le résumé de votre activité</p>

      <div style={styles.grille}>
        <div style={{...styles.carte, borderTop: '4px solid #3498db'}}>
          <p style={styles.carteLabel}>Total négociations</p>
          <p style={styles.carteValeur}>{data.negotiations.total}</p>
        </div>
        <div style={{...styles.carte, borderTop: '4px solid #2ecc71'}}>
          <p style={styles.carteLabel}>Acceptées</p>
          <p style={styles.carteValeur}>{data.negotiations.acceptees}</p>
        </div>
        <div style={{...styles.carte, borderTop: '4px solid #e74c3c'}}>
          <p style={styles.carteLabel}>Refusées</p>
          <p style={styles.carteValeur}>{data.negotiations.refusees}</p>
        </div>
        <div style={{...styles.carte, borderTop: '4px solid #f39c12'}}>
          <p style={styles.carteLabel}>En cours</p>
          <p style={styles.carteValeur}>{data.negotiations.en_cours}</p>
        </div>
      </div>

      <div style={styles.grille2}>
        <div style={styles.carteGrande}>
          <p style={styles.carteLabel}>Chiffre d'affaires</p>
          <p style={{...styles.carteValeur, color: '#2ecc71'}}>
            {data.chiffre_affaires.total_fcfa.toLocaleString()} FCFA
          </p>
        </div>
        <div style={styles.carteGrande}>
          <p style={styles.carteLabel}>Taux de succès</p>
          <p style={{...styles.carteValeur, color: '#3498db'}}>
            {data.negotiations.taux_succes}%
          </p>
        </div>
        <div style={styles.carteGrande}>
          <p style={styles.carteLabel}>Produits actifs</p>
          <p style={styles.carteValeur}>{data.produits_actifs}</p>
        </div>
        <div style={styles.carteGrande}>
          <p style={styles.carteLabel}>Abonnement</p>
          <p style={{...styles.carteValeur, fontSize: '18px', color: '#9b59b6'}}>
            {data.abonnement.plan}
          </p>
          <p style={{fontSize: '12px', color: '#999'}}>
            Expire le {new Date(data.abonnement.date_fin).toLocaleDateString('fr-FR')}
          </p>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { padding: '30px' },
  titre: { fontSize: '24px', color: '#2c3e50', marginBottom: '4px' },
  sousTitre: { color: '#7f8c8d', marginBottom: '30px' },
  chargement: { textAlign: 'center', marginTop: '50px', color: '#666' },
  grille: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '20px',
    marginBottom: '20px',
  },
  grille2: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '20px',
  },
  carte: {
    background: 'white',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.08)',
    textAlign: 'center',
  },
  carteGrande: {
    background: 'white',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.08)',
    textAlign: 'center',
  },
  carteLabel: { color: '#7f8c8d', fontSize: '13px', marginBottom: '8px' },
  carteValeur: { fontSize: '28px', fontWeight: '700', color: '#2c3e50', margin: 0 },
};