import React, { useState, useEffect } from 'react';

export default function GestioneProdotti({ idUtenteLoggato }) {
    const [prodotti, setProdotti] = useState([]);
    const [categorie, setCategorie] = useState([]);
    const [mostraForm, setMostraForm] = useState(false);

    // Campi del form (Stati) basati sul database
    const [idSelezionato, setIdSelezionato] = useState(null);
    const [sigla, setSigla] = useState('');
    const [descrizione, setDescrizione] = useState('');
    const [link, setLink] = useState('');
    const [codiceBarre, setCodiceBarre] = useState('');
    const [idCategoria, setIdCategoria] = useState('');
    const [dataScadenza, setDataScadenza] = useState('');
    useEffect(() => {
        caricaProdotti();
        caricaCategorie();
    }, []);

    const caricaProdotti = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/magazzino/prodotti');
            const data = await res.json();
            setProdotti(data);
        } catch (err) {
            console.error("Errore caricamento prodotti:", err);
        }
    };

    const caricaCategorie = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/magazzino/categorie');
            const data = await res.json();
            setCategorie(data);
            if (data.length > 0 && !idCategoria) setIdCategoria(data[0].id.toString());
        } catch (err) {
            console.error("Errore caricamento categorie:", err);
        }
    };

    const handleSalva = async (e) => {
        e.preventDefault();

        const url = idSelezionato
            ? `http://localhost:5000/api/magazzino/prodotti/${idSelezionato}`
            : 'http://localhost:5000/api/magazzino/prodotti';
        const method = idSelezionato ? 'PUT' : 'POST';

        const corpo = {
            sigla,
            descrizione: descrizione || null,
            link: link || null,
            codice_a_barre: codiceBarre || "000000000000", // Valore di fallback se non fornito
            id_categoria: parseInt(idCategoria),
            id_utente_creatore: idUtenteLoggato, // Fallback admin
            data_scadenza: dataScadenza || null
        };

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(corpo)
            });

            if (response.ok) {
                resetForm();
                caricaProdotti();
            } else {
                const data = await response.json();
                alert(data.message || 'Errore durante il salvataggio');
            }
        } catch (err) {
            console.error("Errore nel salvataggio:", err);
        }
    };

    const avviaModifica = (p) => {
        setIdSelezionato(p.id);
        setSigla(p.sigla);
        setDescrizione(p.descrizione || '');
        setLink(p.link || '');
        setCodiceBarre(p.codice_a_barre || '');
        setIdCategoria(p.id_categoria ? p.id_categoria.toString() : '');
        // Se la data c'è sul DB, la taglia al formato YYYY-MM-DD per l'input HTML, altrimenti stringa vuota
        setDataScadenza(p.data_scadenza ? p.data_scadenza.substring(0, 10) : '');
        setMostraForm(true);
    };

    const handleElimina = async (id) => {
        if (!window.confirm("Sei sicuro di voler eliminare questo prodotto?")) return;

        try {
            const response = await fetch(`http://localhost:5000/api/magazzino/prodotti/${id}`, {
                method: 'DELETE'
            });
            const data = await response.json();

            if (response.ok) {
                caricaProdotti();
            } else {
                alert(data.message);
            }
        } catch (err) {
            console.error("Errore nella cancellazione:", err);
        }
    };

    const resetForm = () => {
        setIdSelezionato(null);
        setSigla('');
        setDescrizione('');
        setLink('');
        setCodiceBarre('');
        if (categorie.length > 0) setIdCategoria(categorie[0].id.toString());
        setMostraForm(false);
        setDataScadenza('');
    };

    return (
        <div style={{ padding: '10px', fontFamily: 'sans-serif' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                {/*<h2>📋 Anagrafica e Gestione Prodotti</h2>*/}
                {!mostraForm && (
                    <button onClick={() => setMostraForm(true)} style={btnNuovoStyle}>
                        ➕ Nuovo Prodotto
                    </button>
                )}
            </div>

            {/* FORM DI INSERIMENTO / MODIFICA */}
            {mostraForm && (
                <form onSubmit={handleSalva} style={formStyle}>
                    <h3>{idSelezionato ? '✏️ Modifica Prodotto' : '📋 Censimento Nuovo Prodotto'}</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px' }}>
                        <div>
                            <label style={{ fontWeight: 'bold' }}>Sigla Prodotto (Univoca):</label>
                            <input type="text" value={sigla} onChange={(e) => setSigla(e.target.value)} style={inputStyle} placeholder="Es. SERVO_DRIVE_01" required />
                        </div>
                        <div>
                            <label style={{ fontWeight: 'bold' }}>Codice a Barre:</label>
                            <input
                                type="text"
                                value={codiceBarre}
                                onChange={(e) => setCodiceBarre(e.target.value)}
                                style={inputStyle}
                                placeholder="Es. 801234567890"
                                required
                            />
                        </div>
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ fontWeight: 'bold' }}>Data di Scadenza (Opzionale):</label>
                        <input
                            type="date"
                            value={dataScadenza}
                            onChange={(e) => setDataScadenza(e.target.value)}
                            style={inputStyle} // Usa lo stesso stile degli altri input
                        />
                    </div>
                    <div style={{ marginBottom: '15px' }}>
                        <label style={{ fontWeight: 'bold' }}>Descrizione Estesa </label>
                        <input
                            type="text"
                            value={descrizione}
                            onChange={(e) => setDescrizione(e.target.value)}
                            style={inputStyle}
                            placeholder="Es. computer portatili"
                            required
                        />
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '20px' }}>
                        <div>
                            <label style={{ fontWeight: 'bold' }}>Link Documentazione / Datasheet:</label>
                            <input type="url" value={link} onChange={(e) => setLink(e.target.value)} style={inputStyle} placeholder="https://example.com/datasheet.pdf" />
                        </div>
                        <div>
                            <label style={{ fontWeight: 'bold' }}>Categoria:</label>
                            <select value={idCategoria} onChange={(e) => setIdCategoria(e.target.value)} style={inputStyle} required>
                                {categorie.map(c => (
                                    <option key={c.id} value={c.id}>{c.descrizione}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <button type="submit" style={btnSalvaStyle}>Salva Prodotto</button>
                    <button type="button" onClick={resetForm} style={btnAnnullaStyle}>Annulla</button>
                </form>
            )}

            {/* TABELLA PRODOTTI ATTUALI */}
            <table style={tableStyle}>
                <thead>
                    <tr style={{ backgroundColor: '#343a40', color: 'white', textAlign: 'left' }}>
                        <th style={thTdStyle}>ID</th>
                        <th style={thTdStyle}>Sigla</th>
                        <th style={thTdStyle}>Descrizione</th>
                        <th style={thTdStyle}>Codice a Barre</th>
                        <th style={thTdStyle}>Link</th>
                        <th style={thTdStyle}>Categoria</th>
                        <th style={thTdStyle}>Scadenza</th>
                        <th style={thTdStyle}>Azioni</th>
                    </tr>
                </thead>
                <tbody>
                    {prodotti.length === 0 ? (
                        <tr>
                            <td colSpan="7" style={{ padding: '20px', textAlign: 'center', color: '#999' }}>Nessun prodotto censito nel magazzino.</td>
                        </tr>
                    ) : (
                        prodotti.map((p) => (
                            <tr key={p.id} style={{ borderBottom: '1px solid #dee2e6' }}>
                                <td style={thTdStyle}><strong>{p.id}</strong></td>
                                <td style={thTdStyle}><code style={{ fontSize: '14px', color: '#e83e8c' }}>{p.sigla}</code></td>
                                <td style={thTdStyle}>{p.descrizione || <em style={{ color: '#bbb' }}>Nessuna descrizione</em>}</td>
                                <td style={thTdStyle}>{p.codice_a_barre || '---'}</td>
                                <td style={thTdStyle}>
                                    {p.link ? (
                                        <a href={p.link} target="_blank" rel="noopener noreferrer" style={{ color: '#007bff', textDecoration: 'none', fontWeight: 'bold' }}>🌐 Apri Link</a>
                                    ) : '---'}
                                </td>
                                <td style={thTdStyle}><span style={badgeStyle}>{p.categoria || 'Generica'}</span></td>
                                <td style={thTdStyle}>
                                    {p.data_scadenza
                                        ? new Date(p.data_scadenza).toLocaleDateString('it-IT')
                                        : <em style={{ color: '#ccc' }}>Nessuna</em>}
                                </td>
                                <td style={thTdStyle}>
                                    <div style={{ display: 'flex', gap: '5px' }}>
                                        <button onClick={() => avviaModifica(p)} style={btnModificaStyle}>✏️ Modifica</button>
                                        <button onClick={() => handleElimina(p.id)} style={btnEliminaStyle}>🗑️ Elimina</button>
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
const btnNuovoStyle = { padding: '10px 15px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' };
const btnSalvaStyle = { padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginRight: '10px', fontWeight: 'bold' };
const btnAnnullaStyle = { padding: '10px 15px', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' };
const btnModificaStyle = { padding: '6px 10px', backgroundColor: '#ffc107', color: 'black', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' };
const btnEliminaStyle = { padding: '6px 10px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' };
const badgeStyle = { padding: '4px 8px', backgroundColor: '#e2e3e5', color: '#383d41', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold' };