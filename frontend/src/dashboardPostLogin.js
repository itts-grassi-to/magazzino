import React, { useState } from 'react';
import GestioneUtenti from './gestioneUtenti';
import GestioneMovimenti from './gestioneMovimenti';
import GestioneProdotti from './gestioneProdotti';
import GestioneAsset from './gestioneAsset';
import GestioneTools from './gestioneTools';

export default function DashboardPostLogin({ utente, onLogout }) {
    const [paginaAttiva, setPaginaAttiva] = useState('dashboard');

    return (
        // Cambiato il flex-direction in 'column' per mettere la barra SOPRA e il contenuto SOTTO
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', fontFamily: 'sans-serif', margin: '-20px' }}>

            {/* 1. NAVBAR ORIZZONTALE SUPERIORE */}
            <div style={{
                backgroundColor: '#2c3e50',
                color: 'white',
                padding: '10px 30px',
                boxSizing: 'border-box',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
                zIndex: 10
            }}>
                {/* Logo e Titolo a sinistra */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <h2 style={{ margin: 0, paddingRight: '20px', borderRight: '1px solid #34495e' }}>📦 Magazzino</h2>

                    {/* MENU DI NAVIGAZIONE ORIZZONTALE */}
                    <ul style={{ listStyleType: 'none', padding: 0, margin: 0, display: 'flex', gap: '10px' }}>
                        <li>
                            <button
                                onClick={() => setPaginaAttiva('dashboard')}
                                style={btnMenuStyle(paginaAttiva === 'dashboard')}
                            >
                                🏠 Home
                            </button>
                        </li>

                        {(utente.ruolo === 'OPERATORE' || utente.ruolo === 'MANAGER' || utente.ruolo === 'ADMIN') && (
                            <li>
                                <button
                                    onClick={() => setPaginaAttiva('movimenti')}
                                    style={btnMenuStyle(paginaAttiva === 'movimenti')}
                                >
                                    📥 Ingressi / Uscite
                                </button>
                            </li>
                        )}

                        {(utente.ruolo === 'MANAGER' || utente.ruolo === 'ADMIN') && (
                            <li>
                                <button
                                    onClick={() => setPaginaAttiva('prodotti')}
                                    style={btnMenuStyle(paginaAttiva === 'prodotti')}
                                >
                                    🗂️ Prodotti
                                </button>
                            </li>
                        )}

                        {/* Voce di menu per l'Anagrafica Asset */}
                        {(utente.ruolo === 'MANAGER' || utente.ruolo === 'ADMIN') && (
                            <li>
                                <button
                                    onClick={() => setPaginaAttiva('asset')}
                                    style={btnMenuStyle(paginaAttiva === 'asset')}
                                >
                                    🏢 Asset
                                </button>
                            </li>
                        )}

                        {utente.ruolo === 'ADMIN' && (
                            <li>
                                <button
                                    onClick={() => setPaginaAttiva('utenti')}
                                    style={btnMenuStyle(paginaAttiva === 'utenti')}
                                >
                                    👥 Utenti
                                </button>
                            </li>
                        )}
                    </ul>
                </div>

                {/* Dati utente connesso e Logout a destra */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <p style={{ fontSize: '14px', color: '#bdc3c7', margin: 0, textAlign: 'right' }}>
                        Utente: <strong>{utente.username}</strong> ({utente.ruolo})
                    </p>
                    <button onClick={onLogout} style={btnLogoutStyle}>Disconnetti</button>
                </div>
            </div>

            {/* 2. AREA CONTENUTO CENTRALE (Ora occupa il 100% della larghezza) */}
            <div style={{ flex: 1, padding: '40px', backgroundColor: '#f8f9fa' }}>
                {paginaAttiva === 'dashboard' && (
                    /*  <div> 
                            <h1>Benvenuto nel Pannello Controllo</h1> 
                            <p style={{ color: '#555' }}>Seleziona una voce dal menu in alto per iniziare a lavorare.</p>
                        </div> 
                    */

                    <div>
                        <GestioneTools />
                    </div>
                )}

                {paginaAttiva === 'prodotti' && (
                    <div>
                        <h1>📥 Gestione Anagrafica Prodotti</h1>
                        <GestioneProdotti idUtenteLoggato={utente.id} />
                    </div>
                )}

                {paginaAttiva === 'movimenti' && (
                    <div>
                        <h1>📥 Gestione Ingressi / Uscite Prodotti</h1>
                        <GestioneMovimenti />
                    </div>
                )}

                {paginaAttiva === 'asset' && (
                    <div>
                        <GestioneAsset />
                    </div>
                )}

                {paginaAttiva === 'utenti' && utente.ruolo === 'ADMIN' && (
                    <div>
                        <h1>👥 Gestione Utenti (Area Riservata Admin)</h1>
                        <GestioneUtenti />
                    </div>
                )}
            </div>
        </div>
    );
}

// ---- STILI INLINE AGGIORNATI PER NAVBAR ORIZZONTALE ----
const btnMenuStyle = (isActive) => ({
    padding: '8px 16px',
    backgroundColor: isActive ? '#3498db' : 'transparent',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '15px',
    transition: 'background 0.2s',
    outline: 'none',
    fontWeight: isActive ? 'bold' : 'normal'
});

const btnLogoutStyle = {
    padding: '8px 16px',
    backgroundColor: '#e74c3c',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 'bold'
};