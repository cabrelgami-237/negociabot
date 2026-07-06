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
    getConversations(commercant_id).then(res => setConversations(res.data));
    getProduits(commercant_id).then(res => setProduits(res.data));
  }, []);

  const chargerHistorique = (conv) => {
    setConvSelectionnee(conv);
    getHistorique(conv.id).then(res => setHistorique(res.data));
  };

  const handleTest = async (e) => {
    e.preventDefault();
    try {
      const res = await envoyerMessage(commercant_id, form);
      setReponse(res.data);
      getConversations(commercant_id).then(r => setConversations(r.data));
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
    <div style={styles.container}>
      <div style={styles.entete}>
        <h2 style={styles.titre}>Négociations</h2>
        <button style={styles.boutonTest} onClick={() => setShowTest(!showTest)}>
          {showTest ? 'Fermer' : '🤖 Tester le bot'}
        </button>
      </div>

      {showTest && (
        <div style={styles.formulaire}>
          <h3 style={styles.formTitre}>Simuler une négociation client</h3>
          <form onSubmit={handleTest}>
            <div style={styles.grille2}>
              <div style={styles.champ}>
                <label style={styles.label}>Produit *</label>
                <select style={styles.input} value={form.produit_id}
                  onChange={e => setForm({...form, produit_id: e.target.value})} required>
                  <option value="">Choisir un produit</option>
                  {produits.map(p => (
                    <option key={p.id} value={p.id}>{p.nom} — {p.prix_affiche.toLocaleString()} FCFA</option>
                  ))}
                </select>
              </div>
              <div style={styles.champ}>
                <label style={styles.label}>Téléphone client *</label>
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
            <button style={styles.boutonEnvoyer} type="submit">
              Envoyer au bot ➤
            </button>
          </form>

          {reponse && (
            <div style={styles.reponseBot}>
              <p style={styles.reponseTitre}>🤖 Réponse du bot :</p>
              <p style={styles.reponseTexte}>{reponse.reponse_bot}</p>
              <div style={styles.reponseInfo}>
                {reponse.prix_propose && (
                  <span style={styles.badge}>Prix proposé : {reponse.prix_propose.toLocaleString()} FCFA</span>
                )}
                <span style={{...styles.badge, background: statutCouleur(reponse.statut), color: 'white'}}>
                  {reponse.statut}
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      <div style={styles.colonnes}>
        <div style={styles.listeConv}>
          <h3 style={styles.sousTitre}>Conversations ({conversations.length})</h3>
          {conversations.length === 0 ? (
            <p style={styles.vide}>Aucune conversation</p>
          ) : (
            conversations.map(conv => (
              <div key={conv.id}
                style={{...styles.carteConv, border: convSelectionnee?.id === conv.id ? '2px solid #0f3460' : '2px solid transparent'}}
                onClick={() => chargerHistorique(conv)}>
                <div style={styles.convEntete}>
                  <span style={styles.clientNom}>{conv.client_nom || 'Client'}</span>
                  <span style={{...styles.statut, background: statutCouleur(conv.statut)}}>
                    {conv.statut}
                  </span>
                </div>
                <p style={styles.clientTel}>📱 {conv.client_telephone}</p>
                {conv.prix_final && (
                  <p style={styles.prixFinal}>✅ {conv.prix_final.toLocaleString()} FCFA</p>
                )}
              </div>
            ))
          )}
        </div>

        <div style={styles.historique}>
          {convSelectionnee ? (
            <>
              <h3 style={styles.sousTitre}>
                Historique — {convSelectionnee.client_nom || 'Client'}
              </h3>
              <div style={styles.messages}>
                {historique.map(msg => (
                  <div key={msg.id} style={{
                    ...styles.message,
                    alignSelf: msg.expediteur === 'BOT' ? 'flex-start' : 'flex-end',
                    background: msg.expediteur === 'BOT' ? '#f0f4ff' : '#0f3460',
                    color: msg.expediteur === 'BOT' ? '#333' : 'white',
                  }}>
                    <span style={styles.expediteur}>
                      {msg.expediteur === 'BOT' ? '🤖 NégociaBot' : '👤 Client'}
                    </span>
                    <p style={styles.messageTexte}>{msg.contenu}</p>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p style={styles.vide}>Sélectionnez une conversation</p>
          )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { padding: '30px' },
  entete: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px' },
  titre: { fontSize: '24px', color: '#2c3e50', margin: 0 },
  boutonTest: {
    padding: '10px 20px', background: 'linear-gradient(135deg, #0f3460, #e94560)',
    color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600'
  },
  formulaire: {
    background: 'white', borderRadius: '12px', padding: '25px',
    marginBottom: '25px', boxShadow: '0 2px 10px rgba(0,0,0,0.08)'
  },
  formTitre: { color: '#2c3e50', marginTop: 0, marginBottom: '20px' },
  grille2: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' },
  champ: { marginBottom: '15px' },
  label: { display: 'block', marginBottom: '6px', fontWeight: '600', color: '#555', fontSize: '13px' },
  input: {
    width: '100%', padding: '10px 12px', border: '2px solid #e0e0e0',
    borderRadius: '8px', fontSize: '14px', boxSizing: 'border-box'
  },
  boutonEnvoyer: {
    padding: '12px 30px', background: '#0f3460', color: 'white',
    border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '700'
  },
  reponseBot: {
    marginTop: '20px', background: '#f0f4ff', borderRadius: '10px',
    padding: '15px', borderLeft: '4px solid #0f3460'
  },
  reponseTitre: { fontWeight: '700', color: '#0f3460', marginBottom: '8px', marginTop: 0 },
  reponseTexte: { fontSize: '16px', color: '#333', marginBottom: '10px' },
  reponseInfo: { display: 'flex', gap: '10px' },
  badge: {
    padding: '4px 12px', background: '#e0e8ff', color: '#0f3460',
    borderRadius: '20px', fontSize: '13px', fontWeight: '600'
  },
  colonnes: { display: 'grid', gridTemplateColumns: '300px 1fr', gap: '20px' },
  listeConv: { background: 'white', borderRadius: '12px', padding: '20px', boxShadow: '0 2px 10px rgba(0,0,0,0.08)' },
  sousTitre: { fontSize: '16px', color: '#2c3e50', marginTop: 0, marginBottom: '15px' },
  vide: { color: '#999', textAlign: 'center', marginTop: '30px' },
  carteConv: {
    padding: '12px', borderRadius: '8px', marginBottom: '10px',
    cursor: 'pointer', background: '#f8f9fa'
  },
  convEntete: { display: 'flex', justifyContent: 'space-between', marginBottom: '4px' },
  clientNom: { fontWeight: '600', color: '#2c3e50', fontSize: '14px' },
  statut: { padding: '2px 8px', borderRadius: '10px', fontSize: '11px', color: 'white', fontWeight: '600' },
  clientTel: { color: '#999', fontSize: '12px', margin: '0' },
  prixFinal: { color: '#2ecc71', fontSize: '13px', fontWeight: '700', margin: '4px 0 0 0' },
  historique: {
    background: 'white', borderRadius: '12px', padding: '20px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.08)', minHeight: '300px'
  },
  messages: { display: 'flex', flexDirection: 'column', gap: '12px' },
  message: { maxWidth: '70%', padding: '12px 15px', borderRadius: '12px' },
  expediteur: { fontSize: '11px', fontWeight: '700', opacity: 0.7, display: 'block', marginBottom: '4px' },
  messageTexte: { margin: 0, fontSize: '14px', lineHeight: '1.5' },
};