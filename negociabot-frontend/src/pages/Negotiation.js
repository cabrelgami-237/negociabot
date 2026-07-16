import React, { useState, useEffect } from 'react';
import { getConversations, getHistorique, envoyerMessage, getProduits } from '../services/api';

export default function Negotiation() {
  const [conversations, setConversations] = useState([]);
  const [produits, setProduits] = useState([]);
  const [convSelectionnee, setConvSelectionnee] = useState(null);
  const [historique, setHistorique] = useState([]);
  const [showTest, setShowTest] = useState(false);
  const [form, setForm] = useState({
    produit_id: '', client_telephone: '', client_nom: '', message: ''
  });
  const [reponse, setReponse] = useState(null);
  const commercant_id = localStorage.getItem('commercant_id');

  useEffect(() => {
    getConversations(commercant_id)
      .then(res => setConversations(res.data || []))
      .catch(() => setConversations([]));
    getProduits(commercant_id)
      .then(res => setProduits(res.data || []))
      .catch(() => setProduits([]));
  }, []);

  const chargerHistorique = (conv) => {
    setConvSelectionnee(conv);
    getHistorique(conv.id)
      .then(res => setHistorique(res.data || []))
      .catch(() => setHistorique([]));
  };

  const handleTest = async (e) => {
    e.preventDefault();
    try {
      const res = await envoyerMessage(commercant_id, form);
      setReponse(res.data);
      getConversations(commercant_id)
        .then(r => setConversations(r.data || []))
        .catch(() => setConversations([]));
    } catch (err) {
      alert(err.response?.data?.detail || 'Erreur');
    }
  };

  const statutCouleur = (statut) => {
    if (statut === 'ACCEPTE') return '#2ecc71';
    if (statut === 'REFUSE') return '#e74c3c';
    return '#f39c12';
  };

  return (
    <div className="page-container" style={styles.container}>
      <div className="page-header" style={styles.entete}>
        <h2 style={styles.titre}>Negociations</h2>
        <button className="btn btn-primary" onClick={() => setShowTest(!showTest)}>
          {showTest ? 'Fermer' : 'Tester le bot'}
        </button>
      </div>

      {showTest && (
        <div className="card" style={styles.formulaire}>
          <h3 style={styles.formTitre}>Simuler une negociation client</h3>
          <form onSubmit={handleTest}>
            <div className="grid-2" style={{ marginBottom: '4px' }}>
              <div style={styles.champ}>
                <label style={styles.label}>Produit *</label>
                <select style={styles.input} value={form.produit_id}
                  onChange={e => setForm({...form, produit_id: e.target.value})} required>
                  <option value="">Choisir un produit</option>
                  {produits.map(p => (
                    <option key={p.id} value={p.id}>{p.nom} — {(p.prix_affiche || 0).toLocaleString()} FCFA</option>
                  ))}
                </select>
              </div>
              <div style={styles.champ}>
                <label style={styles.label}>Telephone client *</label>
                <input style={styles.input} value={form.client_telephone}
                  onChange={e => setForm({...form, client_telephone: e.target.value})}
                  placeholder="655001122" required />
              </div>
            </div>
            <div style={styles.champ}>
              <label style={styles.label}>Nom client</label>
              <input style={styles.input} value={form.client_nom}
                onChange={e => setForm({...form, client_nom: e.target.value})}
                placeholder="Mama Biya" />
            </div>
            <div style={styles.champ}>
              <label style={styles.label}>Message client *</label>
              <input style={styles.input} value={form.message}
                onChange={e => setForm({...form, message: e.target.value})}
                placeholder="Combien coute ce produit ? Je propose 18000 FCFA..."
                required />
            </div>
            <button className="btn btn-primary" type="submit">
              Envoyer au bot
            </button>
          </form>

          {reponse && (
            <div style={styles.reponseBot}>
              <p style={styles.reponseTitre}>Reponse du bot</p>
              <p style={styles.reponseTexte}>{reponse.reponse_bot || 'Aucune reponse'}</p>
              <div style={styles.reponseInfo}>
                {reponse.prix_propose && (
                  <span style={styles.badge}>Prix propose : {reponse.prix_propose.toLocaleString()} FCFA</span>
                )}
                <span style={{...styles.badge, background: statutCouleur(reponse.statut), color: 'white'}}>
                  {reponse.statut || 'EN COURS'}
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      <div style={styles.colonnes} className="negociation-colonnes">
        <div className="card" style={styles.listeConv}>
          <h3 style={styles.sousTitre}>Conversations ({conversations.length})</h3>
          {conversations.length === 0 ? (
            <div className="empty-state" style={{ padding: '30px 10px' }}>
              <div className="empty-state-icon"></div>
              <h3 style={{ fontSize: '14px' }}>Aucune conversation</h3>
              <p style={{ fontSize: '13px' }}>Partagez un lien produit sur WhatsApp pour recevoir vos premieres negociations.</p>
            </div>
          ) : (
            conversations.map(conv => (
              <div key={conv.id}
                style={{...styles.carteConv, border: convSelectionnee?.id === conv.id ? '2px solid #1A73E8' : '2px solid transparent'}}
                onClick={() => chargerHistorique(conv)}>
                <div style={styles.convEntete}>
                  <span style={styles.clientNom}>{conv.client_nom || 'Client'}</span>
                  <span style={{...styles.statut, background: statutCouleur(conv.statut)}}>
                    {conv.statut || 'EN COURS'}
                  </span>
                </div>
                <p style={styles.clientTel}>{conv.client_telephone || 'Telephone inconnu'}</p>
                {conv.prix_final && (
                  <p style={styles.prixFinal}>{conv.prix_final.toLocaleString()} FCFA</p>
                )}
              </div>
            ))
          )}
        </div>

        <div className="card" style={styles.historique}>
          {convSelectionnee ? (
            <>
              <h3 style={styles.sousTitre}>
                Historique — {convSelectionnee.client_nom || 'Client'}
              </h3>
              <div style={styles.messages}>
                {historique.length === 0 ? (
                  <div style={{ textAlign: 'center', color: '#94A3B8', padding: '20px' }}>
                    Aucun message dans cette conversation
                  </div>
                ) : (
                  historique.map(msg => (
                    <div key={msg.id} style={{
                      ...styles.message,
                      alignSelf: msg.expediteur === 'BOT' ? 'flex-start' : 'flex-end',
                      background: msg.expediteur === 'BOT' ? '#f0f4ff' : '#0A3D62',
                      color: msg.expediteur === 'BOT' ? '#1E293B' : 'white',
                    }}>
                      <span style={styles.expediteur}>
                        {msg.expediteur === 'BOT' ? 'NegociaBot' : 'Client'}
                      </span>
                      <p style={styles.messageTexte}>{msg.contenu || 'Message vide'}</p>
                    </div>
                  ))
                )}
              </div>
            </>
          ) : (
            <div className="empty-state">
              <div className="empty-state-icon"></div>
              <h3>Selectionnez une conversation</h3>
              <p>Choisissez une conversation dans la liste pour voir l'historique complet des echanges.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { padding: '30px' },
  entete: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px' },
  titre: { fontSize: '26px', color: '#1E293B', margin: 0, fontWeight: 800 },
  formulaire: { marginBottom: '25px' },
  formTitre: { color: '#1E293B', marginTop: 0, marginBottom: '20px', fontSize: '17px' },
  champ: { marginBottom: '15px' },
  label: { display: 'block', marginBottom: '6px', fontWeight: '600', color: '#475569', fontSize: '13px' },
  input: {
    width: '100%', padding: '10px 12px', border: '2px solid #E2E8F0',
    borderRadius: '8px', fontSize: '14px', boxSizing: 'border-box'
  },
  reponseBot: {
    marginTop: '20px', background: '#f0f4ff', borderRadius: '10px',
    padding: '15px', borderLeft: '4px solid #0A3D62'
  },
  reponseTitre: { fontWeight: '700', color: '#0A3D62', marginBottom: '8px', marginTop: 0 },
  reponseTexte: { fontSize: '16px', color: '#1E293B', marginBottom: '10px' },
  reponseInfo: { display: 'flex', gap: '10px', flexWrap: 'wrap' },
  badge: {
    padding: '4px 12px', background: '#e0e8ff', color: '#0A3D62',
    borderRadius: '20px', fontSize: '13px', fontWeight: '600'
  },
  colonnes: { display: 'grid', gridTemplateColumns: '300px 1fr', gap: '20px' },
  listeConv: { padding: '20px' },
  sousTitre: { fontSize: '16px', color: '#1E293B', marginTop: 0, marginBottom: '15px', fontWeight: 700 },
  carteConv: {
    padding: '12px', borderRadius: '8px', marginBottom: '10px',
    cursor: 'pointer', background: '#F8FAFC'
  },
  convEntete: { display: 'flex', justifyContent: 'space-between', marginBottom: '4px' },
  clientNom: { fontWeight: '600', color: '#1E293B', fontSize: '14px' },
  statut: { padding: '2px 8px', borderRadius: '10px', fontSize: '11px', color: 'white', fontWeight: '600' },
  clientTel: { color: '#94A3B8', fontSize: '12px', margin: '0' },
  prixFinal: { color: '#2ecc71', fontSize: '13px', fontWeight: '700', margin: '4px 0 0 0' },
  historique: { padding: '20px', minHeight: '300px' },
  messages: { display: 'flex', flexDirection: 'column', gap: '12px' },
  message: { maxWidth: '70%', padding: '12px 15px', borderRadius: '12px' },
  expediteur: { fontSize: '11px', fontWeight: '700', opacity: 0.7, display: 'block', marginBottom: '4px' },
  messageTexte: { margin: 0, fontSize: '14px', lineHeight: '1.5' },
};