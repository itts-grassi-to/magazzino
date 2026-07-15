const express = require('express');
const router = express.Router();
const { Pool } = require('pg');

const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@db:5432/magazzino'
});

// 1. GET: Recupera la lista di tutti i prodotti (per i menu a tendina o l'anagrafica)
router.get('/prodotti', async (req, res) => {
    try {
        const query = `
            SELECT p.*, c.descrizione AS categoria 
            FROM prodotto p
            LEFT JOIN categoria c ON p.id_categoria = c.id
            ORDER BY p.id DESC
        `;
        const result = await pool.query(query);
        res.json(result.rows);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Errore nel recupero prodotti' });
    }
});

// 2. GET: Recupera lo storico di tutti i movimenti registrati (incluso il luogo di stoccaggio)
router.get('/storico', async (req, res) => {
    try {
        const query = `
            SELECT m.id, m.quantita, m.operazione, m.data_movimento, 
                   p.sigla AS prodotto_sigla, 
                   u.username AS operatore,
                   ao.sigla AS stoccaggio_sigla
            FROM movimenti m
            JOIN prodotto p ON m.id_prodotto = p.id
            JOIN utenti u ON m.id_utente = u.id
            LEFT JOIN asset_older ao ON m.id_asset_older = ao.id
            ORDER BY m.data_movimento DESC
        `;
        const result = await pool.query(query);
        res.json(result.rows);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Errore nel recupero dello storico movimenti' });
    }
});

// 3. POST: Registra un nuovo movimento (CARICO o SCARICO) con stoccaggio
router.post('/registra', async (req, res) => {
    const { id_prodotto, id_utente, id_asset_older, quantita, operazione } = req.body;

    try {
        await pool.query(
            'INSERT INTO movimenti (id_prodotto, id_utente, id_asset_older, quantita, operazione) VALUES ($1, $2, $3, $4, $5)',
            [id_prodotto, id_utente, id_asset_older, quantita, operazione]
        );
        res.status(201).json({ message: 'Movimento registrato con successo!' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Errore durante la registrazione del movimento' });
    }
});

// 4. GET: Recupera la lista dei luoghi di stoccaggio (Asset Older) per i menu a tendina
router.get('/stoccaggi', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM asset_older ORDER BY sigla ASC');
        res.json(result.rows);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Errore nel recupero dei luoghi di stoccaggio' });
    }
});

// 5. GET: Recupera la lista delle categorie (per i menu a tendina della creazione prodotto)
router.get('/categorie', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM categoria ORDER BY descrizione ASC');
        res.json(result.rows);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Errore nel recupero delle categorie' });
    }
});

// 6. POST: Inserisce un NUOVO prodotto nell'anagrafica (Azione del Manager/Admin)
router.post('/prodotti', async (req, res) => {
    const { sigla, descrizione, link,
        codice_a_barre, id_categoria,
        id_utente_creatore, data_scadenza
    } = req.body;
    if (!codice_a_barre || !id_utente_creatore) {
        return res.status(400).json({
            message: 'Errore: Codice a barre e ID Utente Creatore sono campi obbligatori.'
        });
    }
    try {
        // 2. Eseguiamo la query di inserimento mappando i parametri nell'ordine corretto ($1, $2, ecc.)
        await pool.query(
            'INSERT INTO prodotto (sigla, descrizione, link, \
            codice_a_barre, id_categoria, id_utente_creatore,data_scadenza) \
            VALUES ($1, $2, $3, $4, $5, $6,$7)',
            [
                sigla,
                descrizione || null,
                link || null,
                codice_a_barre,
                id_categoria ? parseInt(id_categoria) : null,
                parseInt(id_utente_creatore),
                data_scadenza || null
            ]
        );
        return
        res.status(201).json(
            { message: 'Nuovo prodotto registrato nell\'anagrafica!' }
        );
        //res.status(201).json({ message: 'Nuovo prodotto registrato nell anagrafica!' });
    } catch (error) {
        console.error(error);
        return res.status(500).json(
            {
                message: 'Errore durante la creazione \
                del prodotto ' }
        );
    }
});
router.put('/prodotti/:id', async (req, res) => {
    const { id } = req.params;
    const { sigla, descrizione, link, codice_a_barre,
        id_categoria, id_utente_creatore, data_scadenza
    } = req.body;
    try {
        await pool.query(
            'UPDATE prodotto SET sigla = $1, \
                descrizione = $2, link = $3, \
                 codice_a_barre = $4, id_categoria = $5, \
                 id_utente_creatore = $6, data_scadenza = $7 \
            WHERE id = $8',
            [sigla, descrizione, link, codice_a_barre, id_categoria,
                id_utente_creatore || null, data_scadenza || null, id]
        );
        res.json({ message: 'Prodotto aggiornato con successo!' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Errore durante la modifica del prodotto' });
    }
});

// 8. DELETE: Elimina un prodotto dall'anagrafica (NUOVO ENDPOINT)
router.delete('/prodotti/:id', async (req, res) => {
    const { id } = req.params;
    try {
        // NOTA: Se il prodotto è già stato usato nella tabella 'movimenti', 
        // PostgreSQL bloccherà la cancellazione sollevando un errore di chiave esterna (corretto per l'integrità dei dati!)
        await pool.query('DELETE FROM prodotto WHERE id = $1', [id]);
        res.json({ message: 'Prodotto eliminato dall\'anagrafica!' });
    } catch (error) {
        console.error(error);
        res.status(400).json({ message: 'Impossibile eliminare il prodotto: è associato a dei movimenti in storico.' });
    }
});
module.exports = router; // Esportazione corretta alla fine del file