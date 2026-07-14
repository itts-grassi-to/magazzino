
// Rileva in automatico l'IP del server da cui stai visualizzando la pagina
const API_BASE_URL = `http://${window.location.hostname}:5000`; import React, { useState, useEffect } from 'react';

export default function GestioneUtenti() {
    const [utenti, setUtenti] = useState([]);
    const [mostraForm, setMostraForm] = useState(false);

    // Stati per i campi del form
    const [idSelezionato, setIdSelezionato] = useState(null);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [ruoloId, setRuoloId] = useState('1'); // Default: OPERATORE (id: 1)

    // 1. Carica gli utenti dal database all'avvio
    const caricaUtenti = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${API_BASE_URL}/api/utenti`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();
            if (response.ok) setUtenti(data);
        } catch (err) {
            console.error('Errore nel caricamento utenti:', err);
        }
    };

    useEffect(() => {
        caricaUtenti();
    }, []);

    // 2. Gestione Salva (Sia Nuovo che Modifica)
    const handleSalva = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');

        // Se c'è un idSelezionato facciamo MODIFICA (PUT), altrimenti NUOVO (POST)
        const url = idSelezionato
            ? `${API_BASE_URL}/api/utenti/${idSelezionato}`
            : `${API_BASE_URL}/api/utenti`;
        const method = idSelezionato ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ username, password, ruolo_id: ruoloId })
            });

            if (response.ok) {
                resetForm();
                caricaUtenti(); // Rinfresca la tabella
            } else {
                const data = await response.json();
                alert(data.message || 'Errore durante il salvataggio');
            }
        } catch (err) {
            console.error('Errore nel salvataggio:', err);
        }
    };

    // 3. Gestione Elimina
    const handleElimina = async (id) => {
        if (!window.confirm('Sei sicuro di voler eliminare questo utente?')) return;

        const token = localStorage.getItem('token');
        try {
            const response = await fetch(`${API_BASE_URL}/api/utenti/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                caricaUtenti();
            }
        } catch (err) {
            console.error('Errore nella cancellazione:', err);
        }
    };

    // Attiva la modalità modifica popolando i campi
    const avviaModifica = (utente) => {
        setIdSelezionato(utente.id);
        setUsername(utente.username);
        setPassword(''); // Lasciamo vuota, la inserisce solo se vuole cambiarla
        setRuoloId(utente.ruolo_id.toString());
        setMostraForm(true);
    };

    const resetForm = () => {
        setIdSelezionato(null);
        setUsername('');
        setPassword('');
        setRuoloId('1');
        setMostraForm(false);
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>👥 Gestione Utenti</h2>
                {!mostraForm && (
                    <button onClick={() => setMostraForm(true)} style={btnNuovaStyle}>
                        ➕ Nuovo Utente
                    </button>
                )}
            </div>

            {/* FORM DI CREAZIONE / MODIFICA */}
            {mostraForm && (
                <form onSubmit={handleSalva} style={formStyle}>
                    <h3>{idSelezionato ? '✏️ Modifica Utente' : '👤 Nuovo Utente'}</h3>
                    <div style={{ marginBottom: '10px' }}>
                        <label>Username:</label><br />
                        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} style={inputStyle} required />
                    </div>
                    <div style={{ marginBottom: '10px' }}>
                        <label>Password {idSelezionato && '(lascia vuota per non modificarla)'}:</label><br />
                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={inputStyle} required={!idSelezionato} />
                    </div>
                    <div style={{ marginBottom: '20px' }}>
                        <label>Ruolo:</label><br />
                        <select value={ruoloId} onChange={(e) => setRuoloId(e.target.value)} style={inputStyle}>
                            <option value="1">OPERATORE</option>
                            <option value="2">MANAGER</option>
                            <option value="3">ADMIN</option>
                        </select>
                    </div>
                    <button type="submit" style={btnSalvaStyle}>Salva</button>
                    <button type="button" onClick={resetForm} style={btnAnnullaStyle}>Annulla</button>
                </form>
            )}

            {/* TABELLA UTENTI */}
            <table style={tableStyle}>
                <thead>
                    <tr style={{ backgroundColor: '#ecf0f1', textAlign: 'left' }}>
                        <th style={thTdStyle}>ID</th>
                        <th style={thTdStyle}>Username</th>
                        <th style={thTdStyle}>Ruolo</th>
                        <th style={thTdStyle}>Azioni</th>
                    </tr>
                </thead>
                <tbody>
                    {utenti.map((u) => (
                        <tr key={u.id} style={{ borderBottom: '1px solid #ddd' }}>
                            <td style={thTdStyle}>{u.id}</td>
                            <td style={thTdStyle}>{u.username}</td>
                            <td style={thTdStyle}>
                                <span style={ruoloBadgeStyle(u.ruolo)}>{u.ruolo}</span>
                            </td>
                            <td style={thTdStyle}>
                                <button onClick={() => avviaModifica(u)} style={btnModificaStyle}>✏️ Modifica</button>
                                <button onClick={() => handleElimina(u.id)} style={btnEliminaStyle}>🗑️ Elimina</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

// ---- STILI INLINE ----
const tableStyle = { width: '100%', borderCollapse: 'collapse', marginTop: '10px', backgroundColor: 'white', borderRadius: '4px', overflow: 'hidden', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' };
const thTdStyle = { padding: '12px 15px', borderBottom: '1px solid #e2e8f0' };
const formStyle = { background: 'white', padding: '20px', borderRadius: '6px', marginBottom: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' };
const inputStyle = { width: '100%', padding: '8px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' };
const btnNuovaStyle = { padding: '10px 15px', backgroundColor: '#2ecc71', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' };
const btnSalvaStyle = { padding: '10px 20px', backgroundColor: '#3498db', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginRight: '10px', fontWeight: 'bold' };
const btnAnnullaStyle = { padding: '10px 15px', backgroundColor: '#95a5a6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' };
const btnModificaStyle = { padding: '6px 10px', backgroundColor: '#f39c12', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginRight: '5px' };
const btnEliminaStyle = { padding: '6px 10px', backgroundColor: '#e74c3c', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' };

const ruoloBadgeStyle = (ruolo) => ({
    padding: '4px 8px',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: 'bold',
    backgroundColor: ruolo === 'ADMIN' ? '#f8d7da' : ruolo === 'MANAGER' ? '#cff4fc' : '#e2e3e5',
    color: ruolo === 'ADMIN' ? '#842029' : ruolo === 'MANAGER' ? '#055160' : '#41464b'
});