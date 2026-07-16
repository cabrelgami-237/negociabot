import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const PLANS = [
  {
    id: 'GRATUIT',
    nom: 'Gratuit',
    prix: 0,
    couleur: '#94A3B8',
    fonctionnalites: ['1 produit', '10 négociations/mois', 'Support email']
  },
  {
    id: 'STARTER',
    nom: 'Starter',
    prix: 5000,
    couleur: '#1A73E8',
    fonctionnalites: ['10 produits', '100 négociations/mois', 'WhatsApp bot', 'Support prioritaire']
  },
  {
    id: 'BUSINESS',
    nom: 'Business',
    prix: 15000,
    couleur: '#9b59b6',
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
    <div className="page-container" style={styles.container}>
      <h2 style={styles.titre}>Abonnement & paiement</h2>
      <p style={styles.sousTitre}>Choisissez votre plan et payez avec MTN MoMo ou Orange Money</p>

      <div style={styles.etapes}>
        {['Plan', 'Méthode', 'Paiement', 'Confirmation'].map((label, i) => (
          <div key={i} style={styles.etapeItem}>
            <div style={{
              ...styles.etapeCercle,
              background: etape > i + 1 ? '#2ecc71' : etape === i + 1 ? '#0A3D62' : '#E2E8F0',
              color: etape >= i + 1 ? 'white' : '#94A3B8'
            }}>
              {i + 1}
            </div>
            <span style={{
              ...styles.etapeLabel,
              color: etape === i + 1 ? '#0A3D62' : '#94A3B8',
              fontWeight: etape === i + 1 ? '700' : '400'
            }}>{label}</span>
          </div>
        ))}
      </div>

      {etape === 1 && (
        <div className="grid-3">
          {PLANS.map(plan => (
            <div key={plan.id} className="card" style={{
              border: plan.populaire ? `2px solid ${plan.couleur}` : '2px solid transparent',
              position: 'relative', textAlign: 'center'
            }}>
              {plan.populaire && (
                <div style={{...styles.badge, background: plan.couleur}}>
                  Populaire
                </div>
              )}
              <h3 style={{...styles.planNom, color: plan.couleur}}>{plan.nom}</h3>
              <p style={styles.planPrix}>
                {plan.prix === 0 ? 'Gratuit' : `${plan.prix.toLocaleString()} FCFA/mois`}
              </p>
              <ul style={styles.liste}>
                {plan.fonctionnalites.map((f, i) => (
                  <li key={i} style={styles.listeItem}>{f}</li>
                ))}
              </ul>
              <button
                className="btn btn-block"
                style={{ background: plan.couleur, color: 'white' }}
                onClick={() => choisirPlan(plan)}
              >
                Choisir {plan.nom}
              </button>
            </div>
          ))}
        </div>
      )}

      {etape === 2 && (
        <div className="card" style={styles.carteEtape}>
          <h3 style={styles.etapeTitre}>
            Plan choisi : <span style={{color: '#0A3D62'}}>{planChoisi?.nom}</span> —
            {planChoisi?.prix === 0 ? ' Gratuit' : ` ${planChoisi?.prix.toLocaleString()} FCFA`}
          </h3>

          {planChoisi?.prix === 0 ? (
            <button className="btn btn-block" style={{ background: '#2ecc71', color: 'white' }}
              onClick={() => choisirMethode('gratuit')}>
              Activer gratuitement
            </button>
          ) : (
            <div className="grid-2" style={{ marginBottom: '20px' }}>
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
            Retour
          </button>
        </div>
      )}

      {etape === 3 && (
        <div className="card" style={styles.carteEtape}>
          <h3 style={styles.etapeTitre}>
            {methode === 'mtn_momo' ? 'MTN Mobile Money' : 'Orange Money'}
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
              className="btn btn-block"
              style={{
                background: methode === 'mtn_momo' ? '#ffcc00' : '#ff6600',
                color: methode === 'mtn_momo' ? '#333' : 'white',
                marginBottom: '15px'
              }}
              type="submit"
              disabled={chargement}
            >
              {chargement ? 'Traitement...' : `Payer ${planChoisi?.prix.toLocaleString()} FCFA`}
            </button>
          </form>
          <button style={styles.boutonRetour} onClick={() => setEtape(2)}>
            Retour
          </button>
        </div>
      )}

      {etape === 4 && resultat && (
        <div className="card" style={styles.carteConfirmation}>
          <h3 style={styles.succesTitre}>Paiement réussi</h3>
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
            className="btn btn-block"
            style={{ background: '#2ecc71', color: 'white', marginTop: '20px' }}
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
  titre: { fontSize: '26px', color: '#1E293B', marginBottom: '4px', fontWeight: 800 },
  sousTitre: { color: '#64748B', marginBottom: '30px', fontSize: '15px' },
  etapes: {
    display: 'flex', justifyContent: 'center', alignItems: 'center',
    gap: '30px', marginBottom: '40px', flexWrap: 'wrap'
  },
  etapeItem: { display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' },
  etapeCercle: {
    width: '36px', height: '36px', borderRadius: '50%',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontWeight: '700', fontSize: '14px'
  },
  etapeLabel: { fontSize: '12px' },
  badge: {
    position: 'absolute', top: '-12px', left: '50%',
    transform: 'translateX(-50%)', padding: '4px 16px',
    borderRadius: '20px', color: 'white', fontSize: '12px', fontWeight: '700'
  },
  planNom: { fontSize: '22px', margin: '0 0 8px 0', fontWeight: 800 },
  planPrix: { fontSize: '20px', fontWeight: '700', color: '#1E293B', marginBottom: '20px' },
  liste: { listStyle: 'none', padding: 0, margin: '0 0 25px 0', textAlign: 'left' },
  listeItem: { padding: '6px 0', color: '#475569', fontSize: '14px' },
  carteEtape: { maxWidth: '600px', margin: '0 auto', padding: '35px' },
  etapeTitre: { color: '#1E293B', marginTop: 0, marginBottom: '20px' },
  carteMethode: {
    border: '2px solid #E2E8F0', borderRadius: '12px', padding: '25px',
    textAlign: 'center', cursor: 'pointer', transition: 'border 0.2s'
  },
  logoMethode: {
    width: '60px', height: '60px', borderRadius: '50%', margin: '0 auto 12px',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontWeight: '900', fontSize: '16px'
  },
  methodeNom: { margin: '0 0 6px 0', color: '#1E293B' },
  methodeDesc: { color: '#94A3B8', fontSize: '13px', margin: 0 },
  montantInfo: { color: '#475569', marginBottom: '20px', fontSize: '16px' },
  champ: { marginBottom: '20px' },
  label: { display: 'block', marginBottom: '6px', fontWeight: '600', color: '#475569' },
  input: {
    width: '100%', padding: '12px', border: '2px solid #E2E8F0',
    borderRadius: '8px', fontSize: '15px', boxSizing: 'border-box'
  },
  aide: { color: '#94A3B8', fontSize: '12px', marginTop: '4px', display: 'block' },
  erreur: {
    color: '#e74c3c', background: '#ffeaea', padding: '10px',
    borderRadius: '8px', fontSize: '14px', marginBottom: '15px'
  },
  boutonRetour: {
    background: 'none', border: 'none', color: '#94A3B8',
    cursor: 'pointer', fontSize: '14px', padding: '5px 0'
  },
  carteConfirmation: {
    maxWidth: '500px', margin: '0 auto', textAlign: 'center', padding: '40px'
  },
  succesTitre: { fontSize: '24px', color: '#2ecc71', marginBottom: '10px' },
  succesMessage: { color: '#475569', marginBottom: '25px' },
  infoConfirmation: {
    background: '#F8FAFC', borderRadius: '10px', padding: '15px', marginBottom: '10px'
  },
  infoItem: {
    display: 'flex', justifyContent: 'space-between',
    padding: '8px 0', borderBottom: '1px solid #eee'
  },
  infoLabel: { color: '#94A3B8', fontSize: '14px' },
  infoValeur: { fontWeight: '700', color: '#1E293B', fontSize: '14px' },
};