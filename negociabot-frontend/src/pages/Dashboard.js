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

  if (chargement) return <div className="empty-state"><p>Chargement...</p></div>;
  if (!data) return <div className="empty-state"><p>Erreur de chargement</p></div>;

  return (
    <div className="page-container" style={styles.container}>
      <h2 style={styles.titre}>Bonjour, {nom_boutique || 'Commercant'}</h2>
      <p style={styles.sousTitre}>Voici le resume de votre activite</p>

      <div className="grid-4" style={{ marginBottom: '20px' }}>
        <div className="card" style={{ borderTop: '4px solid #1A73E8', textAlign: 'center' }}>
          <p style={styles.carteLabel}>Total negociations</p>
          <p style={styles.carteValeur}>{data.negotiations?.total ?? 0}</p>
        </div>
        <div className="card" style={{ borderTop: '4px solid #2ecc71', textAlign: 'center' }}>
          <p style={styles.carteLabel}>Acceptees</p>
          <p style={styles.carteValeur}>{data.negotiations?.acceptees ?? 0}</p>
        </div>
        <div className="card" style={{ borderTop: '4px solid #e74c3c', textAlign: 'center' }}>
          <p style={styles.carteLabel}>Refusees</p>
          <p style={styles.carteValeur}>{data.negotiations?.refusees ?? 0}</p>
        </div>
        <div className="card" style={{ borderTop: '4px solid #f39c12', textAlign: 'center' }}>
          <p style={styles.carteLabel}>En cours</p>
          <p style={styles.carteValeur}>{data.negotiations?.en_cours ?? 0}</p>
        </div>
      </div>

      <div className="grid-4">
        <div className="card" style={{ textAlign: 'center' }}>
          <p style={styles.carteLabel}>Chiffre d affaires</p>
          <p style={{ ...styles.carteValeur, color: '#2ecc71' }}>
            {data.chiffre_affaires?.total_fcfa?.toLocaleString() || '0'} FCFA
          </p>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <p style={styles.carteLabel}>Taux de succes</p>
          <p style={{ ...styles.carteValeur, color: '#1A73E8' }}>
            {data.negotiations?.taux_succes ?? 0}%
          </p>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <p style={styles.carteLabel}>Produits actifs</p>
          <p style={styles.carteValeur}>{data.produits_actifs ?? 0}</p>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <p style={styles.carteLabel}>Abonnement</p>
          <p style={{ ...styles.carteValeur, fontSize: '17px', color: '#9b59b6' }}>
            {data.abonnement?.plan || 'Gratuit'}
          </p>
          <p style={{ fontSize: '12px', color: '#94A3B8', margin: 0 }}>
            {data.abonnement?.date_fin
              ? `Expire le ${new Date(data.abonnement.date_fin).toLocaleDateString('fr-FR')}`
              : 'Illimite'}
          </p>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { padding: '30px' },
  titre: { fontSize: '26px', color: '#1E293B', marginBottom: '4px', fontWeight: 800 },
  sousTitre: { color: '#64748B', marginBottom: '30px', fontSize: '15px' },
  carteLabel: { color: '#64748B', fontSize: '13px', marginBottom: '8px', fontWeight: 500 },
  carteValeur: { fontSize: '28px', fontWeight: '800', color: '#1E293B', margin: 0 },
};