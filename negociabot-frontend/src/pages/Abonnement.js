import React, { useState, useEffect } from 'react';
import { getAbonnement, upgradeAbonnement } from '../services/api';

export default function Abonnement() {
  const [abonnement, setAbonnement] = useState(null);
  const [chargement, setChargement] = useState(true);
  const [planChoisi, setPlanChoisi] = useState(null);
  const commercant_id = localStorage.getItem('commercant_id');

  const chargerAbonnement = () => {
    getAbonnement(commercant_id)
      .then(res => {
        setAbonnement(res.data);
        setChargement(false);
      })
      .catch(() => setChargement(false));
  };

  useEffect(() => { chargerAbonnement(); }, []);

  const handleUpgrade = async (plan) => {
    if (!window.confirm(`Passer au plan ${plan} ?`)) return;
    try {
      await upgradeAbonnement(commercant_id, { plan });
      chargerAbonnement();
      alert('Abonnement mis à jour avec succès !');
    } catch (err) {
      alert(err.response?.data?.detail || 'Erreur lors de la mise à jour');
    }
  };

  const plans = [
    {
      id: 'gratuit',
      nom: 'Gratuit',
      prix: '0 FCFA',
      periode: '/mois',
      features: [
        '1 produit',
        '10 negociations/mois',
        'Support email'
      ],
      popular: false,
      color: '#94A3B8'
    },
    {
      id: 'starter',
      nom: 'Starter',
      prix: '5 000 FCFA',
      periode: '/mois',
      features: [
        '10 produits',
        '100 negociations/mois',
        'WhatsApp bot',
        'Support prioritaire'
      ],
      popular: true,
      color: '#1A73E8'
    },
    {
      id: 'business',
      nom: 'Business',
      prix: '15 000 FCFA',
      periode: '/mois',
      features: [
        'Produits illimites',
        'Negociations illimitees',
        'WhatsApp + Facebook',
        'Tableau de bord analytique',
        'Support 24/7'
      ],
      popular: false,
      color: '#0A3D62'
    }
  ];

  const planActuel = abonnement?.plan || 'gratuit';

  return (
    <div className="page-container" style={styles.container}>
      <div style={styles.entete}>
        <h2 style={styles.titre}>Abonnement et Paiement</h2>
        <p style={styles.sousTitre}>
          Choisissez votre plan et payez avec MTN MoMo ou Orange Money
        </p>
      </div>

      {chargement ? (
        <div className="empty-state"><p>Chargement...</p></div>
      ) : (
        <>
          <div className="card" style={styles.statutActuel}>
            <div style={styles.statutInfo}>
              <span style={styles.statutLabel}>Plan actuel</span>
              <span style={{ ...styles.statutValeur, color: plans.find(p => p.id === planActuel)?.color || '#94A3B8' }}>
                {planActuel.toUpperCase()}
              </span>
            </div>
            {abonnement?.date_fin && (
              <div style={styles.statutInfo}>
                <span style={styles.statutLabel}>Expire le</span>
                <span style={styles.statutValeur}>
                  {new Date(abonnement.date_fin).toLocaleDateString('fr-FR', {
                    day: '2-digit',
                    month: 'long',
                    year: 'numeric'
                  })}
                </span>
              </div>
            )}
            {abonnement?.negociations_restantes !== undefined && (
              <div style={styles.statutInfo}>
                <span style={styles.statutLabel}>Negociations restantes</span>
                <span style={{ ...styles.statutValeur, color: abonnement.negociations_restantes > 0 ? '#2ecc71' : '#e74c3c' }}>
                  {abonnement.negociations_restantes}
                </span>
              </div>
            )}
          </div>

          <div style={styles.grille}>
            {plans.map((plan) => {
              const estActif = planActuel === plan.id;
              return (
                <div 
                  key={plan.id} 
                  className="card" 
                  style={{
                    ...styles.carte,
                    borderColor: estActif ? plan.color : '#E2E8F0',
                    borderWidth: estActif ? '3px' : '1px',
                    position: 'relative',
                    transform: 'scale(1)',
                    transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                  }}
                  onMouseEnter={(e) => {
                    if (!estActif) {
                      e.currentTarget.style.transform = 'scale(1.03)';
                      e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.15)';
                    }
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'scale(1)';
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.08)';
                  }}
                >
                  {plan.popular && !estActif && (
                    <div style={styles.badge}>Populaire</div>
                  )}
                  {estActif && (
                    <div style={{ ...styles.badge, backgroundColor: '#2ecc71' }}>Plan actuel</div>
                  )}

                  <h3 style={styles.planNom}>{plan.nom}</h3>
                  <div style={styles.planPrix}>
                    <span style={styles.prix}>{plan.prix}</span>
                    <span style={styles.periode}>{plan.periode}</span>
                  </div>

                  <ul style={styles.features}>
                    {plan.features.map((feature, index) => (
                      <li key={index} style={styles.featureItem}>
                        <span style={styles.check}></span>
                        {feature}
                      </li>
                    ))}
                  </ul>

                  <button
                    className="btn"
                    style={{
                      ...styles.bouton,
                      backgroundColor: estActif ? '#94A3B8' : plan.color,
                      cursor: estActif ? 'default' : 'pointer',
                    }}
                    onClick={() => !estActif && handleUpgrade(plan.id)}
                    disabled={estActif}
                  >
                    {estActif ? 'Plan actuel' : `Choisir ${plan.nom}`}
                  </button>

                  {!estActif && plan.id !== 'gratuit' && (
                    <div style={styles.paiementInfo}>
                      Paiement par MTN MoMo ou Orange Money
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <div className="card" style={styles.etapes}>
            <h4 style={styles.etapesTitre}>Comment payer ?</h4>
            <div style={styles.etapesListe}>
              <div style={styles.etape}>
                <span style={styles.etapeNum}>1</span>
                <span style={styles.etapeTexte}>Choisissez votre plan</span>
              </div>
              <div style={styles.etape}>
                <span style={styles.etapeNum}>2</span>
                <span style={styles.etapeTexte}>Cliquez sur Choisir</span>
              </div>
              <div style={styles.etape}>
                <span style={styles.etapeNum}>3</span>
                <span style={styles.etapeTexte}>Payez avec MTN MoMo ou Orange Money</span>
              </div>
              <div style={styles.etape}>
                <span style={styles.etapeNum}>4</span>
                <span style={styles.etapeTexte}>Votre compte est active instantanement</span>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

const styles = {
  container: { padding: '30px', maxWidth: '1200px', margin: '0 auto' },
  entete: { marginBottom: '30px' },
  titre: { fontSize: '26px', color: '#1E293B', margin: '0 0 4px 0', fontWeight: 800 },
  sousTitre: { color: '#64748B', fontSize: '15px', margin: 0 },
  
  statutActuel: { 
    display: 'flex', 
    justifyContent: 'space-around', 
    padding: '20px', 
    marginBottom: '30px',
    flexWrap: 'wrap',
    gap: '20px',
    background: 'linear-gradient(135deg, #F8FAFC 0%, #ffffff 100%)',
    border: '2px solid #E2E8F0'
  },
  statutInfo: { display: 'flex', flexDirection: 'column', alignItems: 'center' },
  statutLabel: { fontSize: '12px', color: '#94A3B8', fontWeight: 500 },
  statutValeur: { fontSize: '20px', fontWeight: 800, color: '#1E293B', marginTop: '4px' },
  
  grille: { 
    display: 'grid', 
    gridTemplateColumns: 'repeat(3, 1fr)', 
    gap: '24px',
    marginBottom: '30px',
    alignItems: 'stretch',
  },
  carte: { 
    padding: '28px 20px 20px', 
    display: 'flex', 
    flexDirection: 'column', 
    alignItems: 'center',
    position: 'relative',
    borderRadius: '16px',
    background: 'white',
    height: '100%',
    minHeight: '380px',
  },
  badge: {
    position: 'absolute',
    top: '-12px',
    right: '20px',
    background: '#F59E0B',
    color: 'white',
    padding: '4px 16px',
    borderRadius: '20px',
    fontSize: '12px',
    fontWeight: 700,
  },
  planNom: { fontSize: '20px', fontWeight: 700, color: '#1E293B', margin: '0 0 8px 0' },
  planPrix: { display: 'flex', alignItems: 'baseline', gap: '4px', marginBottom: '16px' },
  prix: { fontSize: '28px', fontWeight: 800, color: '#1E293B' },
  periode: { fontSize: '14px', color: '#94A3B8' },
  
  features: { 
    listStyle: 'none', 
    padding: 0, 
    margin: '0 0 20px 0', 
    width: '100%',
    textAlign: 'left',
    flex: 1,
  },
  featureItem: { 
    padding: '6px 0', 
    fontSize: '14px', 
    color: '#475569',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    borderBottom: '1px solid #F1F5F9'
  },
  check: { color: '#2ecc71', fontWeight: 700, fontSize: '16px' },
  
  bouton: { 
    width: '100%', 
    padding: '12px', 
    border: 'none', 
    borderRadius: '10px', 
    color: 'white',
    fontWeight: 700,
    fontSize: '15px',
    transition: 'opacity 0.2s, transform 0.2s',
    marginTop: 'auto',
  },
  paiementInfo: {
    marginTop: '12px',
    fontSize: '12px',
    color: '#64748B',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '6px',
    width: '100%',
  },
  
  etapes: { padding: '24px', background: '#F8FAFC' },
  etapesTitre: { margin: '0 0 16px 0', color: '#1E293B' },
  etapesListe: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' },
  etape: { display: 'flex', alignItems: 'center', gap: '12px' },
  etapeNum: { 
    background: '#1A73E8', 
    color: 'white', 
    width: '28px', 
    height: '28px', 
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 700,
    fontSize: '13px',
    flexShrink: 0
  },
  etapeTexte: { fontSize: '13px', color: '#475569' }
};