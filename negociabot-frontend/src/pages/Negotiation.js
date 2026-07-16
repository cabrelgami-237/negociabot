import React, { useState, useEffect } from 'react';
import { getNegociations, updateNegociation } from '../services/api';

export default function Negotiation() {
  const [negociations, setNegociations] = useState([]);
  const [chargement, setChargement] = useState(true);
  const [filtre, setFiltre] = useState('tous');
  const commercant_id = localStorage.getItem('commercant_id');

  const chargerNegociations = () => {
    getNegociations(commercant_id)
      .then(res => { 
        setNegociations(res.data); 
        setChargement(false); 
      })
      .catch(() => setChargement(false));
  };

  useEffect(() => { chargerNegociations(); }, []);

  const handleAction = async (id, action) => {
    try {
      await updateNegociation(id, { statut: action });
      chargerNegociations();
    } catch (err) {
      alert('Erreur lors de la mise à jour');
    }
  };

  const negociationsFiltrees = negociations.filter(n => {
    if (filtre === 'tous') return true;
    return n.statut === filtre;
  });

  const getColor = (statut) => {
    switch(statut) {
      case 'acceptee': return '#2ecc71';
      case 'refusee': return '#e74c3c';
      case 'en_cours': return '#f39c12';
      default: return '#94A3B8';
    }
  };

  const getLabel = (statut) => {
    switch(statut) {
      case 'acceptee': return 'Acceptée';
      case 'refusee': return 'Refusée';
      case 'en_cours': return 'En cours';
      default: return statut;
    }
  };

  return (
    <div className="page-container" style={styles.container}>
      <div style={styles.entete}>
        <h2 style={styles.titre}>Négociations</h2>
        <div style={styles.filtres}>
          <button 
            className={`btn ${filtre === 'tous' ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setFiltre('tous')}
            style={filtre === 'tous' ? styles.filtreActif : styles.filtreInactif}
          >
            Tous
          </button>
          <button 
            className={`btn ${filtre === 'en_cours' ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setFiltre('en_cours')}
            style={filtre === 'en_cours' ? styles.filtreActif : styles.filtreInactif}
          >
            En cours
          </button>
          <button 
            className={`btn ${filtre === 'acceptee' ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setFiltre('acceptee')}
            style={filtre === 'acceptee' ? styles.filtreActif : styles.filtreInactif}
          >
            Acceptées
          </button>
          <button 
            className={`btn ${filtre === 'refusee' ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setFiltre('refusee')}
            style={filtre === 'refusee' ? styles.filtreActif : styles.filtreInactif}
          >
            Refusées
          </button>
        </div>
      </div>

      {chargement ? (
        <div className="empty-state"><p>Chargement...</p></div>
      ) : negociationsFiltrees.length === 0 ? (
        <div className="empty-state">
          <div style={styles.emptyIcon}>💬</div>
          <h3>Aucune négociation</h3>
          <p style={styles.emptyText}>
            {filtre === 'tous' 
              ? "Vous n'avez pas encore reçu de demandes de négociation. Partagez vos produits sur WhatsApp pour commencer."
              : `Aucune négociation ${getLabel(filtre).toLowerCase()} pour le moment.`}
          </p>
        </div>
      ) : (
        <div style={styles.liste}>
          {negociationsFiltrees.map(n => (
            <div key={n.id} className="card" style={styles.carte}>
              <div style={styles.carteEntete}>
                <div style={styles.carteInfo}>
                  <span style={styles.nomClient}>{n.client_nom || 'Client'}</span>
                  <span style={{ ...styles.statut, backgroundColor: getColor(n.statut) + '20', color: getColor(n.statut) }}>
                    {getLabel(n.statut)}
                  </span>
                </div>
                <span style={styles.date}>
                  {new Date(n.date_creation).toLocaleDateString('fr-FR', { 
                    day: '2-digit', 
                    month: 'short', 
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              </div>

              <div style={styles.produitInfo}>
                <h4 style={styles.produitNom}>{n.produit_nom}</h4>
                <div style={styles.prixDetails}>
                  <div style={styles.prixItem}>
                    <span style={styles.prixLabel}>Prix affiché</span>
                    <span style={styles.prixValeur}>{n.prix_affiche.toLocaleString()} FCFA</span>
                  </div>
                  <div style={styles.prixItem}>
                    <span style={styles.prixLabel}>Offre du client</span>
                    <span style={{ ...styles.prixValeur, color: '#1A73E8', fontWeight: 800 }}>
                      {n.prix_offert.toLocaleString()} FCFA
                    </span>
                  </div>
                  {n.statut === 'en_cours' && (
                    <div style={styles.prixItem}>
                      <span style={styles.prixLabel}>Marge</span>
                      <span style={{ ...styles.prixValeur, color: n.prix_offert > n.prix_cible ? '#2ecc71' : '#f39c12' }}>
                        {Math.round((1 - n.prix_offert / n.prix_affiche) * 100)}% de remise
                      </span>
                    </div>
                  )}
                </div>
              </div>

              {n.message && (
                <div style={styles.messageContainer}>
                  <span style={styles.messageLabel}>Message :</span>
                  <p style={styles.messageTexte}>"{n.message}"</p>
                </div>
              )}

              {n.statut === 'en_cours' && (
                <div style={styles.actions}>
                  <button 
                    className="btn" 
                    style={{ ...styles.btnAccepter }}
                    onClick={() => handleAction(n.id, 'acceptee')}
                  >
                    ✓ Accepter
                  </button>
                  <button 
                    className="btn" 
                    style={{ ...styles.btnRefuser }}
                    onClick={() => handleAction(n.id, 'refusee')}
                  >
                    ✗ Refuser
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { padding: '30px' },
  entete: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px', flexWrap: 'wrap', gap: '15px' },
  titre: { fontSize: '26px', color: '#1E293B', margin: 0, fontWeight: 800 },
  filtres: { display: 'flex', gap: '8px', flexWrap: 'wrap' },
  filtreActif: { background: '#1A73E8', color: 'white', padding: '8px 16px', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 600 },
  filtreInactif: { background: '#F1F5F9', color: '#475569', padding: '8px 16px', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 500 },
  emptyIcon: { fontSize: '48px', marginBottom: '10px' },
  emptyText: { color: '#64748B', maxWidth: '400px', margin: '0 auto' },
  liste: { display: 'flex', flexDirection: 'column', gap: '16px' },
  carte: { padding: '20px' },
  carteEntete: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px', flexWrap: 'wrap', gap: '8px' },
  carteInfo: { display: 'flex', alignItems: 'center', gap: '12px' },
  nomClient: { fontWeight: 700, color: '#1E293B', fontSize: '15px' },
  statut: { padding: '4px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 600, borderRadius: '20px' },
  date: { color: '#94A3B8', fontSize: '13px' },
  produitInfo: { marginBottom: '12px' },
  produitNom: { margin: '0 0 8px 0', fontSize: '15px', color: '#0A3D62' },
  prixDetails: { display: 'flex', gap: '20px', flexWrap: 'wrap' },
  prixItem: { display: 'flex', flexDirection: 'column' },
  prixLabel: { fontSize: '12px', color: '#94A3B8' },
  prixValeur: { fontWeight: 700, color: '#1E293B', fontSize: '15px' },
  messageContainer: { background: '#F8FAFC', padding: '12px', borderRadius: '8px', marginBottom: '12px' },
  messageLabel: { fontSize: '12px', color: '#94A3B8', display: 'block', marginBottom: '4px' },
  messageTexte: { margin: 0, color: '#1E293B', fontSize: '14px' },
  actions: { display: 'flex', gap: '10px', marginTop: '8px' },
  btnAccepter: { background: '#2ecc71', color: 'white', padding: '8px 24px', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 600, flex: 1 },
  btnRefuser: { background: '#e74c3c', color: 'white', padding: '8px 24px', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 600, flex: 1 },
};