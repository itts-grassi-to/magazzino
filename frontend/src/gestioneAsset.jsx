import React, { useState, useEffect } from 'react';

export default function GestioneAsset() {
    const [assets, setAssets] = useState([]);
    const [mostraForm, setMostraForm] = useState(false);

    // Stati della form (Allineati perfettamente a id, sigla, descrizione)
    const [idSelezionato, setIdSelezionato] = useState(null);
    const [sigla, setSigla] = useState('');
    const [descrizione, setDescrizione] = useState('');
    const urlBase = 'http://localhost:5000/api/asset-manager';

    useEffect(() => {
        caricaAssets();
    }, []);

    const caricaAssets = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/asset-manager');
            const data = await res.json();

            // 1. Stampiamo nei log del browser cosa risponde ESATTAMENTE il server
            console.log("DEBUG ASSET - Dati ricevuti dal server:", data);

            // 2. Controlliamo se la risposta è una vera lista (Array) prima di salvarla
            if (Array.isArray(data)) {
                setAssets(data);
            } else {
                console.error("ATTENZIONE: Il server non ha risposto con un array, ma con:", data);
                // Evitiamo il crash impostando una lista vuota temporanea
                setAssets([]);
                if (data.message) {
                    alert("Il server ha risposto con un errore: " + data.message);
                }
            }
        } catch (err) {
            console.error("Errore di rete nel caricamento degli asset:", err);
            setAssets([]);
        }
    };
    const handleSalva = async (e) => {
        e.preventDefault();

        const url = idSelezionato
            ? `${urlBase}/${idSelezionato}`
            : urlBase;
        const method = idSelezionato ? 'PUT' : 'POST';

        const corpo = {
            sigla: sigla,
            descrizione: descrizione || null // Invia null al DB se la casella è vuota
        };

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(corpo)
            });

            if (response.ok) {
                resetForm();
                caricaAssets();
            } else {
                const data = await response.json();
                alert(data.message || 'Errore durante il salvataggio');
            }
        } catch (err) {
            console.error("Errore nel salvataggio dell'asset:", err);
        }
    };

    const avviaModifica = (a) => {
        setIdSelezionato(a.id);
        setSigla(a.sigla);
        setDescrizione(a.descrizione || ''); // Converte null del DB in stringa vuota per React
        setMostraForm(true);
    };

    const handleElimina = async (id) => {
        if (!window.confirm("Sei sicuro di voler eliminare questo asset/destinazione?")) return;

        try {
            const response = await fetch(`${urlBase}/${id}`, {
                method: 'DELETE'
            });
            const data = await response.json();

            if (response.ok) {
                caricaAssets();
            } else {
                alert(data.message);
            }
        } catch (err) {
            console.error("Errore nella cancellazione dell'asset:", err);
        }
    };

    const resetForm = () => {
        setIdSelezionato(null);
        setSigla('');
        setDescrizione('');
        setMostraForm(false);
    };

    return (
        <div style={{ padding: '10px', fontFamily: 'sans-serif' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>🏢 Anagrafica Asset (Destinazioni)</h2>
                {!mostraForm && (
                    <button onClick={() => setMostraForm(true)} style={btnNuovoStyle}>
                        ➕ Nuovo Asset
                    </button>
                )}
            </div>

            {/* FORM NUOVO / MODIFICA */}
            {mostraForm && (
                <form onSubmit={handleSalva} style={formStyle}>
                    <h3>{idSelezionato ? '✏️ Modifica Asset' : '📋 Censimento Nuovo Asset'}</h3>

                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ fontWeight: 'bold' }}>Sigla / Codice Asset (Univoco):</label>
                        <input type="text" value={sigla} onChange={(e) => setSigla(e.target.value)} style={inputStyle} placeholder="Es. ARMADIO_02 o LINEA_MONTAGGIO_C" required />
                    </div>

                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ fontWeight: 'bold' }}>Descrizione Estesa / Posizione:</label>
                        <input type="text" value={descrizione} onChange={(e) => setDescrizione(e.target.value)} style={inputStyle} placeholder="Es. Scaffale metallico secondo piano - Reparto logistica" />
                    </div>

                    <button type="submit" style={btnSalvaStyle}>Salva Asset</button>
                    <button type="button" onClick={resetForm} style={btnAnnullaStyle}>Annulla</button>
                </form>
            )}

            {/* TABELLA ASSET ATTUALI */}
            <table style={tableStyle}>
                <thead>
                    <tr style={{ backgroundColor: '#2c3e50', color: 'white', textAlign: 'left' }}>
                        <th style={thTdStyle}>ID</th>
                        <th style={thTdStyle}>Sigla Asset</th>
                        <th style={thTdStyle}>Descrizione / Note</th>
                        <th style={thTdStyle}>Azioni</th>
                    </tr>
                </thead>
                <tbody>
                    {assets.length === 0 ? (
                        <tr>
                            <td colSpan="4" style={{ padding: '20px', textAlign: 'center', color: '#999' }}>Nessun asset presente nel sistema.</td>
                        </tr>
                    ) : (
                        assets.map((a) => (
                            <tr key={a.id} style={{ borderBottom: '1px solid #dee2e6' }}>
                                <td style={thTdStyle}><strong>{a.id}</strong></td>
                                <td style={thTdStyle}><code style={{ fontSize: '14px', color: '#16a085', fontWeight: 'bold' }}>{a.sigla}</code></td>
                                <td style={thTdStyle}>{a.descrizione || <em style={{ color: '#ccc' }}>Nessuna descrizione specificata</em>}</td>
                                <td style={thTdStyle}>
                                    <div style={{ display: 'flex', gap: '5px' }}>
                                        <button onClick={() => avviaModifica(a)} style={btnModificaStyle}>✏️ Modifica</button>
                                        <button onClick={() => handleElimina(a.id)} style={btnEliminaStyle}>🗑️ Elimina</button>
                                    </div>
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}

// ---- STILI INLINE ----
const tableStyle = { width: '100%', borderCollapse: 'collapse', marginTop: '10px', backgroundColor: 'white', boxShadow: '0 2px 5px rgba(0,0,0,0.05)' };
const thTdStyle = { padding: '12px', border: '1px solid #dee2e6' };
const formStyle = { background: '#f8f9fa', padding: '20px', borderRadius: '8px', border: '1px solid #e9ecef', marginBottom: '20px' };
const inputStyle = { width: '100%', padding: '8px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' };
const btnNuovoStyle = { padding: '10px 15px', backgroundColor: '#16a085', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' };
const btnSalvaStyle = { padding: '10px 20px', backgroundColor: '#2ecc71', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginRight: '10px', fontWeight: 'bold' };
const btnAnnullaStyle = { padding: '10px 15px', backgroundColor: '#95a5a6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' };
const btnModificaStyle = { padding: '6px 10px', backgroundColor: '#f39c12', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' };
const btnEliminaStyle = { padding: '6px 10px', backgroundColor: '#e74c3c', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' };