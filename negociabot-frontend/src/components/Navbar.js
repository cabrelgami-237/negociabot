import React from 'react';
import logo from '../assets/logo-negociabot.jpeg';

const LIENS = [
  { id: 'dashboard', label: 'Tableau de bord', court: 'Accueil' },
  { id: 'produits', label: 'Produits', court: 'Produits' },
  { id: 'negotiation', label: 'Négociations', court: 'Négoc.' },
  { id: 'abonnement', label: 'Abonnement', court: 'Abonn.' },
];

export default function Navbar({ page, setPage, onLogout }) {
  return (
    <>
      {/* Sidebar desktop */}
      <div className="sidebar">
        <div className="sidebar-logo">
          <img src={logo} alt="NégociaBot" />
        </div>
        <nav className="sidebar-nav">
          {LIENS.map(lien => (
            <button
              key={lien.id}
              className={`sidebar-link ${page === lien.id ? 'active' : ''}`}
              onClick={() => setPage(lien.id)}
            >
              {lien.label}
            </button>
          ))}
        </nav>
        <button className="sidebar-logout" onClick={onLogout}>
          Déconnexion
        </button>
      </div>

      {/* Bottom nav mobile */}
      <div className="bottom-nav">
        {LIENS.map(lien => (
          <button
            key={lien.id}
            className={`bottom-nav-link ${page === lien.id ? 'active' : ''}`}
            onClick={() => setPage(lien.id)}
          >
            <span className="bottom-nav-dot" />
            {lien.court}
          </button>
        ))}
      </div>
    </>
  );
}