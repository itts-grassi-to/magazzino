import React, { useState, useEffect } from 'react';

export default function GestioneMovimenti() {
    // Stati per i dati del form
    const [prodotti, setProdotti] = useState([]);
    const [stoccaggi, setStoccaggi] = useState([]);
    const [storico, setStorico] = useState([]);

    // Campi del modulo
    const [idProdotto, setIdProdotto] = useState('');
    const [idAssetOlder, setIdAssetOlder] = useState('');
    const [quantita, setQuantita] = useState('');
    const [operazione, setOperazione] = useState('INGRESSO');

    // Stati di controllo UI
    const [messaggio, setMessaggio] = useState({ testo: '', tipo: '' });
    const [utenteCorrente, setUtenteCorrente] = useState(null);

    // Recuperiamo i dati iniziali al caricamento del componente
    useEffect(() => {
        // Estraiamo i dati dell'utente loggato salvati nel localStorage o simulati dal token
        const token = localStorage.getItem('token');
        if (token) {
            // Decodifica grossolana del JWT per ottenere l'utente corrente (id e username)
            try {
                const base64Url = token.split('.')[1];
                const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                }).join(''));
                const decoded = JSON.parse(jsonPayload);
                setUtenteCorrente(decoded);
            } catch (e) {
                console.error("Errore decodifica token", e);
            }
        }

        caricaProdotti();
        caricaStoccaggi();
        caricaStorico();
    }, []);

    const caricaProdotti = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/magazzino/prodotti');
            const data = await res.json();
            setProdotti(data);
        } catch (err) {
            console.error("Errore caricamento prodotti", err);
        }
    };

    const caricaStoccaggi = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/magazzino/stoccaggi');
            const data = await res.json();
            setStoccaggi(data);
        } catch (err) {
            console.error("Errore caricamento stoccaggi", err);
        }
    };

    const caricaStorico = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/magazzino/storico');
            const data = await res.json();
            setStorico(data);
        } catch (err) {
            console.error("Errore caricamento storico", err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessaggio({ testo: '', tipo: '' });

        if (!idProdotto || !idAssetOlder || !quantita) {
            setMessaggio({ testo: 'Compilare tutti i campi obbligatori', tipo: 'danger' });
            return;
        }

        const corpoRichiesta = {
            id_prodotto: parseInt(idProdotto),
            id_utente: utenteCorrente ? utenteCorrente.id : 1, // Fallback su ID 1 (admin) se non rilevato
            id_asset_older: parseInt(idAssetOlder),
            quantita: parseInt(quantita),
            operazione: operazione
        };

        try {
            const response = await fetch('http://localhost:5000/api/magazzino/registra', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(corpoRichiesta)
            });

            const data = await response.json();

            if (response.ok) {
                setMessaggio({ testo: `Movimento di ${operazione} registrato con successo!`, tipo: 'success' });
                // Reset form parziale
                setQuantita('');
                caricaStorico(); // Ricarica la tabella dello storico aggiornata
            } else {
                throw new Error(data.message || 'Errore durante la registrazione');
            }
        } catch (err) {
            setMessaggio({ testo: err.message, tipo: 'danger' });
        }
    };

    return (
        <div style={{ padding: '10px', fontFamily: 'sans-serif' }}>
            {/*<h2 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                📦 Area Movimentazione Merci (Carico / Scarico)
            </h2>
            <p style={{ color: '#666' }}>
                Qui gli operatori autorizzati possono registrare gli ingressi e le uscite dei prodotti associandoli alle specifiche aree di stoccaggio.
            </p>*/}

            {messaggio.testo && (
                <div style={{
                    padding: '12px',
                    marginBottom: '20px',
                    borderRadius: '4px',
                    backgroundColor: messaggio.tipo === 'success' ? '#d4edda' : '#f8d7da',
                    color: messaggio.tipo === 'success' ? '#155724' : '#721c24',
                    border: `1px solid ${messaggio.tipo === 'success' ? '#c3e6cb' : '#f5c6cb'}`
                }}>
                    {messaggio.testo}
                </div>
            )}

            {/* SEZIONE FORM DI INSERIMENTO */}
            <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '8px', border: '1px solid #e9ecef', marginBottom: '30px' }}>
                <h4 style={{ margin: '0 0 15px 0' }}>➕ Registra Nuovo Movimento</h4>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexWrap: 'wrap', gap: '15px', alignItems: 'flex-end' }}>

                    <div style={{ flex: '1', minWidth: '200px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', fontSize: '14px' }}>Prodotto (Sigla):</label>
                        <select value={idProdotto} onChange={(e) => setIdProdotto(e.target.value)} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }} required>
                            <option value="">-- Seleziona Prodotto --</option>
                            {prodotti.map(p => (
                                <option key={p.id} value={p.id}>{p.sigla} ({p.categoria || 'Nessuna Categoria'})</option>
                            ))}
                        </select>
                    </div>

                    <div style={{ flex: '1', minWidth: '200px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', fontSize: '14px' }}>Destinazione / Stoccaggio (Asset Older):</label>
                        <select value={idAssetOlder} onChange={(e) => setIdAssetOlder(e.target.value)} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }} required>
                            <option value="">-- Seleziona Posizione --</option>
                            {stoccaggi.map(s => (
                                <option key={s.id} value={s.id}>{s.sigla} - {s.descrizione}</option>
                            ))}
                        </select>
                    </div>

                    <div style={{ width: '120px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', fontSize: '14px' }}>Quantità:</label>
                        <input type="number" min="1" value={quantita} onChange={(e) => setQuantita(e.target.value)} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }} placeholder="Es. 10" required />
                    </div>

                    <div style={{ width: '150px' }}>
                        <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', fontSize: '14px' }}>Tipo Operazione:</label>
                        <select value={operazione} onChange={(e) => setOperazione(e.target.value)} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', fontWeight: 'bold', color: operazione === 'INGRESSO' ? 'green' : 'red' }}>
                            <option value="INGRESSO" style={{ color: 'green', fontWeight: 'bold' }}>📥 INGRESSO (Carico)</option>
                            <option value="USCITA" style={{ color: 'red', fontWeight: 'bold' }}>📤 USCITA (Scarico)</option>
                        </select>
                    </div>

                    <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#007BFF', color: 'white', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer', height: '38px' }}>
                        Esegui Azione
                    </button>
                </form>
            </div>

            {/* TABELLA DELLO STORICO DEI MOVIMENTI */}
            <div>
                <h4 style={{ margin: '0 0 15px 0' }}>📜 Registro Storico Flussi (Carichi e Scarichi)</h4>
                <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px', boxShadow: '0 2px 5px rgba(0,0,0,0.05)' }}>
                    <thead>
                        <tr style={{ backgroundColor: '#343a40', color: 'white', textAlign: 'left' }}>
                            <th style={{ padding: '12px', border: '1px solid #dee2e6' }}>ID</th>
                            <th style={{ padding: '12px', border: '1px solid #dee2e6' }}>Data / Ora</th>
                            <th style={{ padding: '12px', border: '1px solid #dee2e6' }}>Prodotto</th>
                            <th style={{ padding: '12px', border: '1px solid #dee2e6' }}>Tipo</th>
                            <th style={{ padding: '12px', border: '1px solid #dee2e6' }}>Q.tà</th>
                            <th style={{ padding: '12px', border: '1px solid #dee2e6' }}>Ubicazione (Asset)</th>
                            <th style={{ padding: '12px', border: '1px solid #dee2e6' }}>Operatore</th>
                        </tr>
                    </thead>
                    <tbody>
                        {storico.length === 0 ? (
                            <tr>
                                <td colSpan="7" style={{ padding: '20px', textAlign: 'center', color: '#999' }}>Nessun movimento registrato nel registro storico.</td>
                            </tr>
                        ) : (
                            storico.map((m) => (
                                <tr key={m.id} style={{ borderBottom: '1px solid #dee2e6', backgroundColor: m.operazione === 'INGRESSO' ? '#f4fbf7' : '#fffbfb' }}>
                                    <td style={{ padding: '12px', border: '1px solid #dee2e6', fontWeight: 'bold' }}>{m.id}</td>
                                    <td style={{ padding: '12px', border: '1px solid #dee2e6', fontSize: '14px' }}>{new Date(m.data_movimento).toLocaleString('it-IT')}</td>
                                    <td style={{ padding: '12px', border: '1px solid #dee2e6', fontWeight: '500' }}>{m.prodotto_sigla}</td>
                                    <td style={{ padding: '12px', border: '1px solid #dee2e6' }}>
                                        <span style={{
                                            padding: '4px 8px',
                                            borderRadius: '4px',
                                            fontSize: '12px',
                                            fontWeight: 'bold',
                                            backgroundColor: m.operazione === 'INGRESSO' ? '#d4edda' : '#f8d7da',
                                            color: m.operazione === 'INGRESSO' ? '#155724' : '#721c24',
                                        }}>
                                            {m.operazione}
                                        </span>
                                    </td>
                                    <td style={{ padding: '12px', border: '1px solid #dee2e6', fontWeight: 'bold' }}>{m.quantita}</td>
                                    <td style={{ padding: '12px', border: '1px solid #dee2e6' }}><code style={{ color: '#0056b3', fontWeight: 'bold' }}>{m.stoccaggio_sigla}</code></td>
                                    <td style={{ padding: '12px', border: '1px solid #dee2e6', color: '#555' }}>👤 {m.operatore}</td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}