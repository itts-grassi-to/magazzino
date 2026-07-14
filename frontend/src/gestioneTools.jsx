// Rileva in automatico l'IP del server da cui stai visualizzando la pagina
const API_BASE_URL = `http://${window.location.hostname}:5000`;
import React, { useState, useEffect } from 'react';

export default function GestioneTools() {
    // Stato per decidere quale STRUMENTO specifico mostrare dentro la Dashboard dei Tools
    const [toolAttiva, setToolAttiva] = useState('ricercaScorte');

    // --- Stati per il Tool 1: Ricerca Scorte ---
    const [risultati, setRisultati] = useState([]);
    const [termine, setTermine] = useState('');
    const [categoriaSel, setCategoriaSel] = useState('');
    const [categorie, setCategorie] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        caricaCategorie();
        eseguiRicerca();
    }, []);

    const caricaCategorie = async () => {
        try {
            const res = await fetch(`${API_BASE_URL}/api/magazzino/categorie`);
            const data = await res.json();
            if (Array.isArray(data)) setCategorie(data);
        } catch (err) {
            console.error(err);
        }
    };

    const eseguiRicerca = async (e) => {
        if (e) e.preventDefault();
        setLoading(true);
        try {
            const queryParams = new URLSearchParams({ termine, id_categoria: categoriaSel }).toString();
            const res = await fetch(`${API_BASE_URL}/api/tools/scorte?${queryParams}`);
            const data = await res.json();
            if (Array.isArray(data)) setRisultati(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setTermine('');
        setCategoriaSel('');
        setTimeout(() => {
            fetch(`${API_BASE_URL}/api/tools/scorte`).then(r => r.json()).then(d => setRisultati(d));
        }, 50);
    };

    return (
        <div style={{ fontFamily: 'sans-serif' }}>
            {/* INTESTAZIONE DELLA DASHBOARD DEGLI STRUMENTI */}
            <div style={{ marginBottom: '25px' }}>
                <h1>🛠️ Dashboard di Controllo Strumenti (V1.0)</h1>
                <p style={{ color: '#555' }}>Centrale operativa per l'analisi dei dati, diagnostica e monitoraggio magazzino.</p>
            </div>

            {/* SELETTORE DELLE STRUMENTI (TAB INTERNE) */}
            <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '2px solid #e4e7eb', paddingBottom: '10px' }}>
                <button
                    onClick={() => setToolAttiva('ricercaScorte')}
                    style={tabToolStyle(toolAttiva === 'ricercaScorte')}
                >
                    📊 1. Ricerca Giacenze & Scorte
                </button>

                {/* PREPARAZIONE PER I PROSSIMI MODULI IN V2.0 */}
                <button
                    disabled
                    style={{ ...tabToolStyle(false), opacity: 0.5, cursor: 'not-allowed' }}
                    title="Disponibile nelle prossime versioni"
                >
                    ⚠️ 2. Analisi Scadenze (In Arrivo)
                </button>
                <button
                    disabled
                    style={{ ...tabToolStyle(false), opacity: 0.5, cursor: 'not-allowed' }}
                >
                    📈 3. Statistiche Flussi (In Arrivo)
                </button>
            </div>

            {/* CONTENUTO DELLO STRUMENTO SELEZIONATO */}
            {toolAttiva === 'ricercaScorte' && (
                <div>
                    {/* FILTRI DI RICERCA */}
                    <div style={{ background: '#f1f2f6', padding: '20px', borderRadius: '8px', marginBottom: '20px', border: '1px solid #e4e7eb' }}>
                        <form onSubmit={eseguiRicerca} style={{ display: 'flex', gap: '15px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
                            <div style={{ flex: 2, minWidth: '250px' }}>
                                <label style={{ fontSize: '13px', fontWeight: 'bold', color: '#444' }}>Cerca per Codici o Parole Chiave nella descrizione:</label>
                                <input
                                    type="text"
                                    placeholder="Es: bullone, PROD-01, 800123..."
                                    value={termine}
                                    onChange={(e) => setTermine(e.target.value)}
                                    style={inputStyle}
                                />
                            </div>
                            <div style={{ flex: 1, minWidth: '180px' }}>
                                <label style={{ fontSize: '13px', fontWeight: 'bold', color: '#444' }}>Filtro Categoria:</label>
                                <select value={categoriaSel} onChange={(e) => setCategoriaSel(e.target.value)} style={inputStyle}>
                                    <option value="">-- Tutte le Categorie --</option>
                                    {categorie.map(c => <option key={c.id} value={c.id}>{c.descrizione}</option>)}
                                </select>
                            </div>
                            <div style={{ display: 'flex', gap: '10px' }}>
                                <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#3498db', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>Cerca</button>
                                <button type="button" onClick={handleReset} style={{ padding: '10px 15px', backgroundColor: '#a4b0be', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Reset</button>
                            </div>
                        </form>
                    </div>

                    {/* TABELLA DATI */}
                    <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 5px rgba(0,0,0,0.05)' }}>
                        {loading ? (
                            <p style={{ textAlign: 'center', color: '#666' }}>Elaborazione scorte...</p>
                        ) : risultati.length === 0 ? (
                            <p style={{ textAlign: 'center', color: '#999', padding: '20px' }}>Nessun record trovato.</p>
                        ) : (
                            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                <thead>
                                    <tr style={{ backgroundColor: '#f8f9fa', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>
                                        <th style={{ padding: '12px' }}>Sigla</th>
                                        <th style={{ padding: '12px' }}>Codice a Barre</th>
                                        <th style={{ padding: '12px' }}>Categoria</th>
                                        <th style={{ padding: '12px' }}>Descrizione</th>
                                        <th style={{ padding: '12px' }}>Scadenza</th>
                                        <th style={{ padding: '12px', textAlign: 'center' }}>Scorta Disponibile</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {risultati.map(p => {
                                        const scaduto = p.data_scadenza && new Date(p.data_scadenza) < new Date();
                                        const qty = parseInt(p.scorta_attuale);
                                        return (
                                            <tr key={p.id} style={{ borderBottom: '1px solid #dee2e6' }}>
                                                <td style={{ padding: '12px', fontWeight: 'bold' }}>{p.sigla}</td>
                                                <td style={{ padding: '12px' }}><code>{p.codice_a_barre}</code></td>
                                                <td style={{ padding: '12px' }}><span style={{ backgroundColor: '#dfe4ea', padding: '4px 8px', borderRadius: '4px', fontSize: '13px' }}>{p.categoria || 'Nessuna'}</span></td>
                                                <td style={{ padding: '12px', color: '#555', maxWidth: '250px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={p.descrizione}>{p.descrizione || <em>Nessuna</em>}</td>
                                                <td style={{ padding: '12px', color: scaduto ? '#d9534f' : '#333', fontWeight: scaduto ? 'bold' : 'normal' }}>
                                                    {p.data_scadenza ? new Date(p.data_scadenza).toLocaleDateString('it-IT') : '--'}
                                                    {scaduto && ' ⚠️ SCADUTO'}
                                                </td>
                                                <td style={{ padding: '12px', textAlign: 'center' }}>
                                                    <span style={{
                                                        padding: '6px 12px', borderRadius: '20px', fontWeight: 'bold',
                                                        backgroundColor: qty > 10 ? '#d4edda' : qty > 0 ? '#fff3cd' : '#f8d7da',
                                                        color: qty > 10 ? '#155724' : qty > 0 ? '#856404' : '#721c24'
                                                    }}>{qty} pz</span>
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

// Stili locali
const tabToolStyle = (isActive) => ({
    padding: '10px 20px',
    backgroundColor: isActive ? '#2c3e50' : '#f1f2f6',
    color: isActive ? 'white' : '#2c3e50',
    border: '1px solid #ccc',
    borderBottom: 'none',
    borderRadius: '4px 4px 0 0',
    cursor: 'pointer',
    fontWeight: 'bold',
    fontSize: '14px'
});
const inputStyle = { width: '100%', padding: '10px', marginTop: '5px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box', fontSize: '14px' };