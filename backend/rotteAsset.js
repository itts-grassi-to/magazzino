const express = require('express');
const router = express.Router();

const { Pool } = require('pg');
const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@db:5432/magazzino'
});
//module.exports = pool;
// 1. GET: Recupera tutti gli asset censiti
router.get('/', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM asset_older ORDER BY id DESC');
        res.json(result.rows);
    } catch (error) {
        console.error("Errore recupero asset:", error);
        res.status(500).json({ message: 'Errore durante il recupero degli asset' });
    }
});

// 2. POST: Inserisce un NUOVO asset
router.post('/', async (req, res) => {
    const { sigla, descrizione } = req.body;
    try {
        await pool.query(
            'INSERT INTO asset_older (sigla, descrizione) VALUES ($1, $2)',
            [sigla, descrizione]
        );
        res.status(201).json({ message: 'Nuovo asset registrato con successo!' });
    } catch (error) {
        console.error("Errore creazione asset:", error);
        res.status(500).json({ message: 'Errore durante la creazione dell\'asset (verifica che la sigla non esista già)' });
    }
});

// 3. PUT: Modifica un asset esistente
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { sigla, descrizione } = req.body;
    try {
        await pool.query(
            'UPDATE asset_older SET sigla = $1, descrizione = $2 WHERE id = $3',
            [sigla, descrizione, id]
        );
        res.json({ message: 'Asset aggiornato con successo!' });
    } catch (error) {
        console.error("Errore modifica asset:", error);
        res.status(500).json({ message: 'Errore durante la modifica dell\'asset' });
    }
});

// 4. DELETE: Elimina un asset dall'anagrafica
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    try {
        // Se l'asset è già usato nella tabella movimenti, Postgres bloccherà l'azione
        await pool.query('DELETE FROM asset_older WHERE id = $1', [id]);
        res.json({ message: 'Asset eliminato dall\'anagrafica con successo!' });
    } catch (error) {
        console.error("Errore eliminazione asset:", error);
        res.status(400).json({ message: 'Impossibile eliminare l\'asset: è associato a dei movimenti storici.' });
    }
});

module.exports = router;