import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const PLANS = [
  {
    id: 'GRATUIT',
    nom: 'Gratuit',
    prix: 0,
    couleur: '#95a5a6',
    icone: '🆓',
    fonctionnalites: ['1 produit', '10 négociations/mois', 'Support email']
  },
  {
    id: 'STARTER',
    nom: 'Starter',
    prix: 5000,
    couleur: '#3498db',
    icone: '🚀',
    fonctionnalites: ['10 produits', '100 négociations/mois', 'WhatsApp bot', 'Support prioritaire']
  },
  {
    id: 'BUSINESS',
    nom: 'Business',
    prix: 15000,
    couleur: '#9b59b6',
    icone: '💼',
    populaire: true,
    fonctionnalites: ['Produits illimités', 'Négociations illimitées', 'WhatsApp + Facebook', 'Tableau de bord analytique', 'Support 24/7']
  }
];

export default function Paiement() {
  const [planChoisi, setPlanChoisi] = useState(null);
  const [methode, setMethode] = useState(null);
  const [telephone, setTelephone] = useState('');
  const [etape, setEtape] = useState(1);
  const [chargement, setChargement] = useState(false);
  const [resultat, setResultat] = useState(null);
  const [erreur, setErreur] = useState('');
  const commercant_id = localStorage.getItem('commercant_id');

  const choisirPlan = (plan) => {
    setPlanChoisi(plan);
    setEtape(2);
    setErreur('');
  };

  const choisirMethode = (m) => {
    setMethode(m);
    setEtape(3);
    setErreur('');
  };

  const handlePaiement = async (e) => {
    e.preventDefault();
    setChargement(true);
    setErreur('');

    try {
      const endpoint = methode === 'mtn_momo'
        ? `${API_URL}/paiement/momo/initier`
        : `${API_URL}/paiement/orange/initier`;

      const res = await axios.post(endpoint, {
        commercant_id,
        telephone,
        plan: planChoisi.id
      });

      const data = res.data;

      if (data.succes) {
        // Confirmer automatiquement en mode simulation
        const confirmEndpoint = methode === 'mtn_momo'
          ? `${API_URL}/paiement/momo/confirmer`
          : `${API_URL}/paiement/orange/confirmer`;

        const confirm = await axios.post(confirmEndpoint, {
          reference: data.reference,
          commercant_id,
          plan: planChoisi.id
        });

        setResultat(confirm.data);
        setEtape(4);
      } else {
        setErreur(data.message || 'Erreur lors du paiement');
      }
    } catch (err) {
      setErreur(err.response?.data?.detail || 'Erreur de connexion');
    }
    setChargement(false);
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.titre}>Abonnement & Paiement</h2>
      <p style={styles.sousTitre}>Choisissez votre plan et payez avec MTN MoMo ou Orange Money</p>

      {/* Indicateur d'étapes */}
      <div style={styles.etapes}>
        {['Plan', 'Méthode', 'Paiement', 'Confirmation'].map((label, i) => (
          <div key={i} style={styles.etapeItem}>
            <div style={{
              ...styles.etapeCercle,
              background: etape > i + 1 ? '#2ecc71' : etape === i + 1 ? '#0f3460' : '#ddd',
              color: etape >= i + 1 ? 'white' : '#999'
            }}>
              {etape > i + 1 ? '✓' : i + 1}
            </div>
            <span style={{
              ...styles.etapeLabel,
              color: etape === i + 1 ? '#0f3460' : '#999',
              fontWeight: etape === i + 1 ? '700' : '400'
            }}>{label}</span>
          </div>
        ))}
      </div>

      {/* Étape 1 — Choisir le plan */}
      {etape === 1 && (
        <div style={styles.grille}>
          {PLANS.map(plan => (
            <div key={plan.id} style={{
              ...styles.cartePlan,
              border: `2px solid ${plan.couleur}`,
              position: 'relative'
            }}>
              {plan.populaire && (
                <div style={{...styles.badge, background: plan.couleur}}>
                  ⭐ Populaire
                </div>
              )}
              <div style={{fontSize: '40px', marginBottom: '10px'}}>{plan.icone}</div>
              <h3 style={{...styles.planNom, color: plan.couleur}}>{plan.nom}</h3>
              <p style={styles.planPrix}>
                {plan.prix === 0 ? 'Gratuit' : `${plan.prix.toLocaleString()} FCFA/mois`}
              </p>
              <ul style={styles.liste}>
                {plan.fonctionnalites.map((f, i) => (
                  <li key={i} style={styles.listeItem}>✅ {f}</li>
                ))}
              </ul>
              <button
                style={{...styles.boutonChoisir, background: plan.couleur}}
                onClick={() => choisirPlan(plan)}
              >
                Choisir {plan.nom}
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Étape 2 — Choisir la méthode */}
      {etape === 2 && (
        <div style={styles.carteEtape}>
          <h3 style={styles.etapeTitre}>
            Plan choisi : <span style={{color: '#0f3460'}}>{planChoisi?.nom}</span> —
            {planChoisi?.prix === 0 ? ' Gratuit' : ` ${planChoisi?.prix.toLocaleString()} FCFA`}
          </h3>

          {planChoisi?.prix === 0 ? (
            <button style={{...styles.boutonChoisir, background: '#2ecc71', width: '100%'}}
              onClick={() => choisirMethode('gratuit')}>
              Activer gratuitement
            </button>
          ) : (
            <div style={styles.grilleMethodes}>
              <div style={styles.carteMethode} onClick={() => choisirMethode('mtn_momo')}>
                <div style={{...styles.logoMethode, background: '#ffcc00', color: '#333'}}>
                  MTN
                </div>
                <h4 style={styles.methodeNom}>MTN Mobile Money</h4>
                <p style={styles.methodeDesc}>Préfixes : 650-679</p>
              </div>
              <div style={styles.carteMethode} onClick={() => choisirMethode('orange_money')}>
                <div style={{...styles.logoMethode, background: '#ff6600', color: 'white'}}>
                  OM
                </div>
                <h4 style={styles.methodeNom}>Orange Money</h4>
                <p style={styles.methodeDesc}>Préfixes : 655-699</p>
              </div>
            </div>
          )}
          <button style={styles.boutonRetour} onClick={() => setEtape(1)}>
            ← Retour
          </button>
        </div>
      )}

      {/* Étape 3 — Saisir le téléphone */}
      {etape === 3 && (
        <div style={styles.carteEtape}>
          <h3 style={styles.etapeTitre}>
            {methode === 'mtn_momo' ? '📱 MTN Mobile Money' : '📱 Orange Money'}
          </h3>
          <p style={styles.montantInfo}>
            Montant à payer : <strong>{planChoisi?.prix.toLocaleString()} FCFA</strong>
          </p>
          <form onSubmit={handlePaiement}>
            <div style={styles.champ}>
              <label style={styles.label}>Numéro de téléphone</label>
              <input
                style={styles.input}
                type="tel"
                value={telephone}
                onChange={e => setTelephone(e.target.value)}
                placeholder={methode === 'mtn_momo' ? '6XXXXXXXX (MTN)' : '6XXXXXXXX (Orange)'}
                required
              />
              <small style={styles.aide}>
                {methode === 'mtn_momo'
                  ? 'Numéro MTN commençant par 650-679'
                  : 'Numéro Orange commençant par 655-699'}
              </small>
            </div>
            {erreur && <p style={styles.erreur}>{erreur}</p>}
            <button
              style={{
                ...styles.boutonPayer,
                background: methode === 'mtn_momo' ? '#ffcc00' : '#ff6600',
                color: methode === 'mtn_momo' ? '#333' : 'white'
              }}
              type="submit"
              disabled={chargement}
            >
              {chargement ? 'Traitement...' : `Payer ${planChoisi?.prix.toLocaleString()} FCFA`}
            </button>
          </form>
          <button style={styles.boutonRetour} onClick={() => setEtape(2)}>
            ← Retour
          </button>
        </div>
      )}

      {/* Étape 4 — Confirmation */}
      {etape === 4 && resultat && (
        <div style={styles.carteConfirmation}>
          <div style={styles.succes}>✅</div>
          <h3 style={styles.succestitre}>Paiement réussi !</h3>
          <p style={styles.succesMessage}>{resultat.message}</p>
          <div style={styles.infoConfirmation}>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Plan activé</span>
              <span style={styles.infoValeur}>{resultat.plan}</span>
            </div>
            <div style={styles.infoItem}>
              <span style={styles.infoLabel}>Expire le</span>
              <span style={styles.infoValeur}>
                {resultat.date_fin
                  ? new Date(resultat.date_fin).toLocaleDateString('fr-FR')
                  : '-'}
              </span>
            </div>
          </div>
          <button
            style={{...styles.boutonChoisir, background: '#2ecc71', width: '100%', marginTop: '20px'}}
            onClick={() => { setEtape(1); setResultat(null); setPlanChoisi(null); }}
          >
            Retour aux plans
          </button>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { padding: '30px' },
  titre: { fontSize: '24px', color: '#2c3e50', marginBottom: '4px' },
  sousTitre: { color: '#7f8c8d', marginBottom: '30px' },
  etapes: {
    display: 'flex', justifyContent: 'center', alignItems: 'center',
    gap: '30px', marginBottom: '40px'
  },
  etapeItem: { display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' },
  etapeCercle: {
    width: '36px', height: '36px', borderRadius: '50%',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontWeight: '700', fontSize: '14px'
  },
  etapeLabel: { fontSize: '12px' },
  grille: { display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '25px' },
  cartePlan: {
    background: 'white', borderRadius: '16px', padding: '30px',
    textAlign: 'center', boxShadow: '0 4px 15px rgba(0,0,0,0.08)'
  },
  badge: {
    position: 'absolute', top: '-12px', left: '50%',
    transform: 'translateX(-50%)', padding: '4px 16px',
    borderRadius: '20px', color: 'white', fontSize: '12px', fontWeight: '700'
  },
  planNom: { fontSize: '22px', margin: '0 0 8px 0' },
  planPrix: { fontSize: '20px', fontWeight: '700', color: '#2c3e50', marginBottom: '20px' },
  liste: { listStyle: 'none', padding: 0, margin: '0 0 25px 0', textAlign: 'left' },
  listeItem: { padding: '6px 0', color: '#555', fontSize: '14px' },
  boutonChoisir: {
    width: '100%', padding: '12px', color: 'white', border: 'none',
    borderRadius: '8px', cursor: 'pointer', fontWeight: '700', fontSize: '15px'
  },
  carteEtape: {
    background: 'white', borderRadius: '16px', padding: '35px',
    maxWidth: '600px', margin: '0 auto', boxShadow: '0 4px 15px rgba(0,0,0,0.08)'
  },
  etapeTitre: { color: '#2c3e50', marginTop: 0, marginBottom: '20px' },
  grilleMethodes: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' },
  carteMethode: {
    border: '2px solid #e0e0e0', borderRadius: '12px', padding: '25px',
    textAlign: 'center', cursor: 'pointer', transition: 'border 0.2s'
  },
  logoMethode: {
    width: '60px', height: '60px', borderRadius: '50%', margin: '0 auto 12px',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontWeight: '900', fontSize: '16px'
  },
  methodeNom: { margin: '0 0 6px 0', color: '#2c3e50' },
  methodeDesc: { color: '#999', fontSize: '13px', margin: 0 },
  montantInfo: { color: '#555', marginBottom: '20px', fontSize: '16px' },
  champ: { marginBottom: '20px' },
  label: { display: 'block', marginBottom: '6px', fontWeight: '600', color: '#555' },
  input: {
    width: '100%', padding: '12px', border: '2px solid #e0e0e0',
    borderRadius: '8px', fontSize: '15px', boxSizing: 'border-box'
  },
  aide: { color: '#999', fontSize: '12px', marginTop: '4px', display: 'block' },
  erreur: {
    color: '#e74c3c', background: '#ffeaea', padding: '10px',
    borderRadius: '8px', fontSize: '14px', marginBottom: '15px'
  },
  boutonPayer: {
    width: '100%', padding: '14px', border: 'none', borderRadius: '8px',
    cursor: 'pointer', fontWeight: '700', fontSize: '16px', marginBottom: '15px'
  },
  boutonRetour: {
    background: 'none', border: 'none', color: '#999',
    cursor: 'pointer', fontSize: '14px', padding: '5px 0'
  },
  carteConfirmation: {
    background: 'white', borderRadius: '16px', padding: '40px',
    maxWidth: '500px', margin: '0 auto', textAlign: 'center',
    boxShadow: '0 4px 15px rgba(0,0,0,0.08)'
  },
  succes: { fontSize: '60px', marginBottom: '15px' },
  succesître: { fontSize: '24px', color: '#2ecc71', marginBottom: '10px' },
  succesMessage: { color: '#555', marginBottom: '25px' },
  infoConfirmation: {
    background: '#f8f9fa', borderRadius: '10px', padding: '15px', marginBottom: '10px'
  },
  infoItem: {
    display: 'flex', justifyContent: 'space-between',
    padding: '8px 0', borderBottom: '1px solid #eee'
  },
  infoLabel: { color: '#999', fontSize: '14px' },
  infoValeur: { fontWeight: '700', color: '#2c3e50', fontSize: '14px' },
};