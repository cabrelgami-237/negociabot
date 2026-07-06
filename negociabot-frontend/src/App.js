import React, { useState } from 'react';
import Login from './pages/Login';
import Inscription from './pages/Inscription';
import Dashboard from './pages/Dashboard';
import Produits from './pages/Produits';
import Negotiation from './pages/Negotiation';
import Paiement from './pages/Paiement';
import Navbar from './components/Navbar';

export default function App() {
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem('token');
    const commercant_id = localStorage.getItem('commercant_id');
    const nom_boutique = localStorage.getItem('nom_boutique');
    return token ? { token, commercant_id, nom_boutique } : null;
  });
  const [page, setPage] = useState('dashboard');
  const [ecranAuth, setEcranAuth] = useState('login'); // 'login' ou 'inscription'

  const handleLogin = (data) => {
    setUser(data);
    setPage('dashboard');
  };

  const handleLogout = () => {
    localStorage.clear();
    setUser(null);
    setEcranAuth('login');
  };

  if (!user) {
    if (ecranAuth === 'inscription') {
      return (
        <Inscription
          onLogin={handleLogin}
          onRetourLogin={() => setEcranAuth('login')}
        />
      );
    }
    return (
      <Login
        onLogin={handleLogin}
        onInscription={() => setEcranAuth('inscription')}
      />
    );
  }

  const renderPage = () => {
    if (page === 'dashboard') return <Dashboard />;
    if (page === 'produits') return <Produits />;
    if (page === 'negotiation') return <Negotiation />;
    if (page === 'paiement') return <Paiement />;
    return <Dashboard />;
  };

  return (
    <div style={{ display: 'flex' }}>
      <Navbar page={page} setPage={setPage} onLogout={handleLogout} />
      <div style={{ marginLeft: '240px', flex: 1, minHeight: '100vh', background: '#f5f7fb' }}>
        {renderPage()}
      </div>
    </div>
  );
}