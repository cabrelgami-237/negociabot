import React, { useState, useEffect } from 'react';
import { getProduits, creerProduit, supprimerProduit } from '../services/api';

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
    React.createElement('div', {style: styles.container},
      React.createElement('div', {style: styles.entete},
        React.createElement('h2', {style: styles.titre}, 'Mes Produits'),
        React.createElement('button', {style: styles.boutonAjouter, onClick: () => setShowForm(!showForm)},
          showForm ? 'Annuler' : '+ Ajouter un produit'
        )
      ),
      React.createElement('div', {style: styles.configWhatsApp},
        React.createElement('span', {style: styles.configLabel}, 'Ton numero WhatsApp :'),
        React.createElement('input', {
          style: styles.inputTel, type: 'tel', value: telephone,
          onChange: e => setTelephone(e.target.value),
          placeholder: '699001122 (sans +237)'
        }),
        React.createElement('span', {style: styles.configAide}, 'Pour generer les liens WhatsApp')
      ),
      showForm && React.createElement('div', {style: styles.formulaire},
        React.createElement('h3', {style: styles.formTitre}, 'Nouveau produit'),
        React.createElement('form', {onSubmit: handleSubmit},
          React.createElement('div', {style: styles.champ},
            React.createElement('label', {style: styles.label}, 'Nom *'),
            React.createElement('input', {style: styles.input, value: form.nom, onChange: e => setForm({...form, nom: e.target.value}), required: true, placeholder: 'Pagne Wax Holland'})
          ),
          React.createElement('div', {style: styles.champ},
            React.createElement('label', {style: styles.label}, 'Description'),
            React.createElement('input', {style: styles.input, value: form.description, onChange: e => setForm({...form, description: e.target.value}), placeholder: 'Description'})
          ),
          React.createElement('div', {style: styles.grille3},
            React.createElement('div', {style: styles.champ},
              React.createElement('label', {style: styles.label}, 'Prix affiche *'),
              React.createElement('input', {style: styles.input, type: 'number', value: form.prix_affiche, onChange: e => setForm({...form, prix_affiche: e.target.value}), required: true, placeholder: '25000'})
            ),
            React.createElement('div', {style: styles.champ},
              React.createElement('label', {style: styles.label}, 'Prix cible *'),
              React.createElement('input', {style: styles.input, type: 'number', value: form.prix_cible, onChange: e => setForm({...form, prix_cible: e.target.value}), required: true, placeholder: '20000'})
            ),
            React.createElement('div', {style: styles.champ},
              React.createElement('label', {style: styles.label}, 'Prix plancher *'),
              React.createElement('input', {style: styles.input, type: 'number', value: form.prix_plancher, onChange: e => setForm({...form, prix_plancher: e.target.value}), required: true, placeholder: '17000'})
            )
          ),
          React.createElement('button', {style: styles.boutonSoumettre, type: 'submit'}, 'Enregistrer')
        )
      ),
      chargement ? React.createElement('p', {style: styles.chargement}, 'Chargement...') :
      produits.length === 0 ? React.createElement('div', {style: styles.vide}, React.createElement('p', null, 'Aucun produit.')) :
      React.createElement('div', {style: styles.grilleProduits},
        produits.map(p => React.createElement('div', {key: p.id, style: styles.carteProduit},
          React.createElement('div', {style: styles.carteEntete},
            React.createElement('span', {style: styles.categorie}, p.categorie || 'General'),
            React.createElement('button', {style: styles.boutonSupprimer, onClick: () => handleSupprimer(p.id)}, 'X')
          ),
          React.createElement('h3', {style: styles.nomProduit}, p.nom),
          React.createElement('p', {style: styles.description}, p.description || '-'),
          React.createElement('div', {style: styles.prix},
            React.createElement('div', {style: styles.prixItem},
              React.createElement('span', {style: styles.prixLabel}, 'Affiche'),
              React.createElement('span', {style: styles.prixValeur}, p.prix_affiche.toLocaleString() + ' FCFA')
            ),
            React.createElement('div', {style: styles.prixItem},
              React.createElement('span', {style: styles.prixLabel}, 'Cible'),
              React.createElement('span', {style: {...styles.prixValeur, color: '#2ecc71'}}, p.prix_cible.toLocaleString() + ' FCFA')
            ),
            React.createElement('div', {style: styles.prixItem},
              React.createElement('span', {style: styles.prixLabel}, 'Plancher'),
              React.createElement('span', {style: {...styles.prixValeur, color: '#e74c3c'}}, p.prix_plancher.toLocaleString() + ' FCFA')
            )
          ),
          React.createElement('div', {style: styles.sectionWa},
            React.createElement('p', {style: styles.waTitle}, 'Partager sur les reseaux'),
            telephone === '' ?
              React.createElement('p', {style: styles.waAvert}, 'Entre ton numero en haut') :
              React.createElement('div', null,
                React.createElement('button', {style: {...styles.boutonWa, background: '#25D366'}, onClick: () => copierLien(p, 'lien')},
                  copie === p.id + '-lien' ? 'Copie !' : 'Copier lien WhatsApp'
                ),
                React.createElement('button', {style: {...styles.boutonWa, background: '#0f3460', marginTop: '8px'}, onClick: () => copierLien(p, 'publication')},
                  copie === p.id + '-publication' ? 'Copie !' : 'Copier texte publication'
                ),
                React.createElement('a', {href: genererLien(p), target: '_blank', rel: 'noreferrer', style: styles.boutonTester}, 'Tester le lien')
              )
          )
        ))
      )
    )
  );
}

const styles = {
  container: { padding: '30px' },
  entete: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' },
  titre: { fontSize: '24px', color: '#2c3e50', margin: 0 },
  boutonAjouter: { padding: '10px 20px', background: 'linear-gradient(135deg, #0f3460, #e94560)', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' },
  configWhatsApp: { background: 'white', borderRadius: '12px', padding: '15px 20px', marginBottom: '25px', display: 'flex', alignItems: 'center', gap: '12px', boxShadow: '0 2px 10px rgba(0,0,0,0.08)' },
  configLabel: { fontWeight: '600', color: '#2c3e50', whiteSpace: 'nowrap' },
  inputTel: { padding: '8px 12px', border: '2px solid #25D366', borderRadius: '8px', fontSize: '14px', width: '180px' },
  configAide: { color: '#999', fontSize: '13px' },
  formulaire: { background: 'white', borderRadius: '12px', padding: '25px', marginBottom: '25px', boxShadow: '0 2px 10px rgba(0,0,0,0.08)' },
  formTitre: { color: '#2c3e50', marginBottom: '20px', marginTop: 0 },
  grille3: { display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '15px' },
  champ: { marginBottom: '15px' },
  label: { display: 'block', marginBottom: '6px', fontWeight: '600', color: '#555', fontSize: '13px' },
  input: { width: '100%', padding: '10px 12px', border: '2px solid #e0e0e0', borderRadius: '8px', fontSize: '14px', boxSizing: 'border-box' },
  boutonSoumettre: { padding: '12px 30px', background: '#2ecc71', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '700', fontSize: '15px' },
  chargement: { textAlign: 'center', color: '#666', marginTop: '50px' },
  vide: { textAlign: 'center', color: '#999', marginTop: '60px' },
  grilleProduits: { display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' },
  carteProduit: { background: 'white', borderRadius: '12px', padding: '20px', boxShadow: '0 2px 10px rgba(0,0,0,0.08)' },
  carteEntete: { display: 'flex', justifyContent: 'space-between', marginBottom: '10px' },
  categorie: { background: '#eef2ff', color: '#0f3460', padding: '3px 10px', borderRadius: '20px', fontSize: '12px', fontWeight: '600' },
  boutonSupprimer: { background: '#ffe0e0', color: '#e74c3c', border: 'none', borderRadius: '50%', width: '24px', height: '24px', cursor: 'pointer', fontWeight: '700' },
  nomProduit: { fontSize: '16px', color: '#2c3e50', margin: '0 0 6px 0' },
  description: { color: '#999', fontSize: '13px', marginBottom: '15px' },
  prix: { borderTop: '1px solid #f0f0f0', paddingTop: '12px', marginBottom: '15px' },
  prixItem: { display: 'flex', justifyContent: 'space-between', marginBottom: '6px' },
  prixLabel: { color: '#999', fontSize: '13px' },
  prixValeur: { fontWeight: '700', color: '#2c3e50', fontSize: '13px' },
  sectionWa: { borderTop: '1px solid #f0f0f0', paddingTop: '12px' },
  waTitle: { fontWeight: '600', color: '#2c3e50', fontSize: '13px', marginBottom: '10px', marginTop: 0 },
  waAvert: { color: '#f39c12', fontSize: '12px', margin: 0 },
  boutonWa: { width: '100%', padding: '8px', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', fontSize: '13px', display: 'block' },
  boutonTester: { display: 'block', marginTop: '8px', padding: '8px', background: '#f0f4ff', color: '#0f3460', border: '1px solid #0f3460', borderRadius: '8px', textAlign: 'center', textDecoration: 'none', fontSize: '13px', fontWeight: '600' },
};
