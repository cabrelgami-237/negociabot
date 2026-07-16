import React, { useState, useEffect } from 'react';
import { getProduits, creerProduit, supprimerProduit } from '../services/api';

function formaterTelephone(tel) {
  const digits = tel.replace(/\D/g, '');
  if (digits.length !== 9) return tel;
  return `+237 ${digits.slice(0,3)} ${digits.slice(3,5)} ${digits.slice(5,7)} ${digits.slice(7,9)}`;
}

export default function Produits() {
  const [produits, setProduits] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [chargement, setChargement] = useState(true);
  const [telephone, setTelephone] = useState('');
  const [copie, setCopie] = useState(null);
  const [form, setForm] = useState({
    nom: '', description: '', categorie: '',
    prix_affiche: '', prix_cible: '', prix_plancher: '', devise: 'FCFA'
  });
  const commercant_id = localStorage.getItem('commercant_id');
  const nom_boutique = localStorage.getItem('nom_boutique');

  const chargerProduits = () => {
    getProduits(commercant_id)
      .then(res => { setProduits(res.data); setChargement(false); })
      .catch(() => setChargement(false));
  };

  useEffect(() => { chargerProduits(); }, []);

  const genererLien = (produit) => {
    const tel = telephone.replace(/\s/g, '');
    const numero = tel.startsWith('237') ? tel : '237' + tel;
    const msg = encodeURIComponent('Bonjour ! Je veux negocier ' + produit.nom + ' a ' + produit.prix_affiche + ' FCFA chez ' + nom_boutique);
    return 'https://wa.me/' + numero + '?text=' + msg;
  };

  const genererTexte = (produit) => {
    return produit.nom + '\nPrix : ' + produit.prix_affiche + ' FCFA\n\nNegociez sur WhatsApp :\n' + genererLien(produit);
  };

  const copierLien = (produit, type) => {
    const texte = type === 'lien' ? genererLien(produit) : genererTexte(produit);
    navigator.clipboard.writeText(texte);
    setCopie(produit.id + '-' + type);
    setTimeout(() => setCopie(null), 2000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await creerProduit(commercant_id, {
        ...form,
        prix_affiche: parseFloat(form.prix_affiche),
        prix_cible: parseFloat(form.prix_cible),
        prix_plancher: parseFloat(form.prix_plancher),
      });
      setForm({ nom: '', description: '', categorie: '', prix_affiche: '', prix_cible: '', prix_plancher: '', devise: 'FCFA' });
      setShowForm(false);
      chargerProduits();
    } catch (err) {
      alert(err.response?.data?.detail || 'Erreur');
    }
  };

  const handleSupprimer = async (id) => {
    if (window.confirm('Supprimer ce produit ?')) {
      await supprimerProduit(id);
      chargerProduits();
    }
  };

  return (
    <div className="page-container" style={styles.container}>
      <div className="page-header" style={styles.entete}>
        <h2 style={styles.titre}>Mes produits</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Annuler' : 'Ajouter un produit'}
        </button>
      </div>

      <div className="card" style={styles.configWhatsApp}>
        <span style={styles.configLabel}>Votre numero WhatsApp</span>
        <input
          style={styles.inputTel}
          type="tel"
          value={telephone}
          onChange={e => setTelephone(e.target.value)}
          placeholder="699 00 11 22"
        />
        {telephone && <span style={styles.telFormate}>{formaterTelephone(telephone)}</span>}
        <span style={styles.configAide}>Utilise pour generer les liens de negociation WhatsApp</span>
      </div>

      {showForm && (
        <div className="card" style={styles.formulaire}>
          <h3 style={styles.formTitre}>Nouveau produit</h3>
          <form onSubmit={handleSubmit}>
            <div style={styles.champ}>
              <label style={styles.label}>Nom *</label>
              <input style={styles.input} value={form.nom} onChange={e => setForm({...form, nom: e.target.value})} required placeholder="Pagne Wax Holland" />
            </div>
            <div style={styles.champ}>
              <label style={styles.label}>Description</label>
              <input style={styles.input} value={form.description} onChange={e => setForm({...form, description: e.target.value})} placeholder="Description du produit" />
            </div>
            <div className="grid-3" style={{ marginBottom: '10px' }}>
              <div style={styles.champ}>
                <label style={styles.label}>Prix affiche *</label>
                <input style={styles.input} type="number" value={form.prix_affiche} onChange={e => setForm({...form, prix_affiche: e.target.value})} required placeholder="25000" />
              </div>
              <div style={styles.champ}>
                <label style={styles.label}>Prix cible *</label>
                <input style={styles.input} type="number" value={form.prix_cible} onChange={e => setForm({...form, prix_cible: e.target.value})} required placeholder="20000" />
              </div>
              <div style={styles.champ}>
                <label style={styles.label}>Prix plancher *</label>
                <input style={styles.input} type="number" value={form.prix_plancher} onChange={e => setForm({...form, prix_plancher: e.target.value})} required placeholder="17000" />
              </div>
            </div>
            <button className="btn btn-primary" type="submit">Enregistrer</button>
          </form>
        </div>
      )}

      {chargement ? (
        <div className="empty-state"><p>Chargement...</p></div>
      ) : produits.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon"></div>
          <h3>Aucun produit pour l instant</h3>
          <p>Ajoutez votre premier produit pour generer un lien WhatsApp et commencer a recevoir des negociations.</p>
          <button className="btn btn-primary" onClick={() => setShowForm(true)}>Ajouter un produit</button>
        </div>
      ) : (
        <div className="grid-3">
          {produits.map(p => (
            <div key={p.id} className="card">
              <div style={styles.carteEntete}>
                <span style={styles.categorie}>{p.categorie || 'General'}</span>
                <button style={styles.boutonSupprimer} onClick={() => handleSupprimer(p.id)}>×</button>
              </div>
              <h3 style={styles.nomProduit}>{p.nom}</h3>
              <p style={styles.description}>{p.description || '—'}</p>
              <div style={styles.prix}>
                <div style={styles.prixItem}>
                  <span style={styles.prixLabel}>Affiche</span>
                  <span style={styles.prixValeur}>{p.prix_affiche.toLocaleString()} FCFA</span>
                </div>
                <div style={styles.prixItem}>
                  <span style={styles.prixLabel}>Cible</span>
                  <span style={{...styles.prixValeur, color: '#2ecc71'}}>{p.prix_cible.toLocaleString()} FCFA</span>
                </div>
                <div style={styles.prixItem}>
                  <span style={styles.prixLabel}>Plancher</span>
                  <span style={{...styles.prixValeur, color: '#e74c3c'}}>{p.prix_plancher.toLocaleString()} FCFA</span>
                </div>
              </div>
              <div style={styles.sectionWa}>
                <p style={styles.waTitle}>Partager sur les reseaux</p>
                {telephone === '' ? (
                  <p style={styles.waAvert}>Renseignez votre numero ci-dessus</p>
                ) : (
                  <>
                    <button className="btn btn-block" style={{ background: '#25D366', color: 'white', marginBottom: '8px' }} onClick={() => copierLien(p, 'lien')}>
                      {copie === p.id + '-lien' ? 'Copie !' : 'Copier lien WhatsApp'}
                    </button>
                    <button className="btn btn-block" style={{ background: '#0A3D62', color: 'white', marginBottom: '8px' }} onClick={() => copierLien(p, 'publication')}>
                      {copie === p.id + '-publication' ? 'Copie !' : 'Copier texte publication'}
                    </button>
                    <a href={genererLien(p)} target="_blank" rel="noreferrer" style={styles.boutonTester}>
                      Tester le lien
                    </a>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { padding: '30px' },
  entete: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' },
  titre: { fontSize: '26px', color: '#1E293B', margin: 0, fontWeight: 800 },
  configWhatsApp: { marginBottom: '25px', display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' },
  configLabel: { fontWeight: '600', color: '#1E293B', whiteSpace: 'nowrap', fontSize: '14px' },
  inputTel: { padding: '9px 12px', border: '2px solid #25D366', borderRadius: '8px', fontSize: '14px', width: '160px' },
  telFormate: { color: '#25D366', fontWeight: 600, fontSize: '13px' },
  configAide: { color: '#94A3B8', fontSize: '13px' },
  formulaire: { marginBottom: '25px' },
  formTitre: { color: '#1E293B', marginBottom: '20px', marginTop: 0, fontSize: '17px' },
  champ: { marginBottom: '15px' },
  label: { display: 'block', marginBottom: '6px', fontWeight: '600', color: '#475569', fontSize: '13px' },
  input: { width: '100%', padding: '10px 12px', border: '2px solid #E2E8F0', borderRadius: '8px', fontSize: '14px', boxSizing: 'border-box' },
  carteEntete: { display: 'flex', justifyContent: 'space-between', marginBottom: '10px' },
  categorie: { background: '#eef2ff', color: '#0A3D62', padding: '3px 10px', borderRadius: '20px', fontSize: '12px', fontWeight: '600' },
  boutonSupprimer: { background: '#ffe0e0', color: '#e74c3c', border: 'none', borderRadius: '50%', width: '26px', height: '26px', cursor: 'pointer', fontWeight: '700', fontSize: '16px', lineHeight: '1' },
  nomProduit: { fontSize: '16px', color: '#1E293B', margin: '0 0 6px 0', fontWeight: 700 },
  description: { color: '#94A3B8', fontSize: '13px', marginBottom: '15px' },
  prix: { borderTop: '1px solid #F1F5F9', paddingTop: '12px', marginBottom: '15px' },
  prixItem: { display: 'flex', justifyContent: 'space-between', marginBottom: '6px' },
  prixLabel: { color: '#94A3B8', fontSize: '13px' },
  prixValeur: { fontWeight: '700', color: '#1E293B', fontSize: '13px' },
  sectionWa: { borderTop: '1px solid #F1F5F9', paddingTop: '12px' },
  waTitle: { fontWeight: '600', color: '#1E293B', fontSize: '13px', marginBottom: '10px', marginTop: 0 },
  waAvert: { color: '#f39c12', fontSize: '12px', margin: 0 },
  boutonTester: { display: 'block', padding: '9px', background: '#f0f4ff', color: '#0A3D62', border: '1px solid #0A3D62', borderRadius: '8px', textAlign: 'center', textDecoration: 'none', fontSize: '13px', fontWeight: '600' },
};