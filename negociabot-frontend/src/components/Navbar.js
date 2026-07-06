import React from 'react';

export default function Navbar({ page, setPage, onLogout }) {
  const liens = [
    { id: 'dashboard', label: '📊 Tableau de bord' },
    { id: 'produits', label: '📦 Produits' },
    { id: 'negotiation', label: '🤝 Négociations' },
    { id: 'paiement', label: '💳 Abonnement' },
  ];

  return (
    <div style={styles.sidebar}>
      <div style={styles.logo}>
        <h2 style={styles.logoTexte}>🤝 NégociaBot</h2>
        <p style={styles.logoSous}>Négociation IA</p>
      </div>

      <nav style={styles.nav}>
        {liens.map(lien => (
          <button
            key={lien.id}
            style={{
              ...styles.lien,
              background: page === lien.id ? 'rgba(255,255,255,0.2)' : 'transparent',
              fontWeight: page === lien.id ? '700' : '400',
            }}
            onClick={() => setPage(lien.id)}
          >
            {lien.label}
          </button>
        ))}
      </nav>

      <button style={styles.boutonLogout} onClick={onLogout}>
        🚪 Déconnexion
      </button>
    </div>
  );
}

const styles = {
  sidebar: {
    width: '240px',
    minHeight: '100vh',
    background: 'linear-gradient(180deg, #0f3460 0%, #16213e 100%)',
    display: 'flex',
    flexDirection: 'column',
    padding: '0',
    position: 'fixed',
    left: 0,
    top: 0,
  },
  logo: {
    padding: '30px 20px',
    borderBottom: '1px solid rgba(255,255,255,0.1)',
  },
  logoTexte: {
    color: 'white',
    margin: 0,
    fontSize: '20px',
  },
  logoSous: {
    color: 'rgba(255,255,255,0.6)',
    margin: '4px 0 0 0',
    fontSize: '12px',
  },
  nav: {
    flex: 1,
    padding: '20px 10px',
    display: 'flex',
    flexDirection: 'column',
    gap: '5px',
  },
  lien: {
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    padding: '12px 15px',
    textAlign: 'left',
    cursor: 'pointer',
    fontSize: '14px',
    transition: 'background 0.2s',
  },
  boutonLogout: {
    margin: '20px',
    padding: '12px',
    background: 'rgba(233,69,96,0.3)',
    color: 'white',
    border: '1px solid rgba(233,69,96,0.5)',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
  },
};