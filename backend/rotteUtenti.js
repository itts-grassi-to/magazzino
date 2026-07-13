const express = require('express');
const router = express.Router();
const { Pool } = require('pg');
const bcrypt = require('bcrypt');

// Inizializziamo il pool di connessione al database anche qui
const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@db:5432/magazzino'
});

// 1. GET: Legge tutti gli utenti (con una JOIN per prendere il nome del ruolo)
router.get('/', async (req, res) => {
    try {
        const query = `
            SELECT u.id, u.username, u.ruolo_id, r.nome AS ruolo 
            FROM utenti u 
            JOIN ruoli r ON u.ruolo_id = r.id
            ORDER BY u.id ASC
        `;
        const result = await pool.query(query);
        res.json(result.rows);
    } catch (error) {
        console.error('Errore GET utenti:', error);
        res.status(500).json({ message: 'Errore nel recupero degli utenti' });
    }
});

// 2. POST: Crea un nuovo utente (cifrando la password)
router.post('/', async (req, res) => {
    const { username, password, ruolo_id } = req.body;
    try {
        // Controlla se lo username esiste già
        const check = await pool.query('SELECT * FROM utenti WHERE username = $1', [username]);
        if (check.rows.length > 0) {
            return res.status(400).json({ message: 'Username già utilizzato' });
        }

        // Cifra la password con bcrypt
        const saltRounds = 10;
        const hash = await bcrypt.hash(password, saltRounds);

        // Inserisce nel DB
        await pool.query(
            'INSERT INTO utenti (username, password_hash, ruolo_id) VALUES ($1, $2, $3)',
            [username, hash, ruolo_id]
        );
        res.status(201).json({ message: 'Utente creato con successo!' });
    } catch (error) {
        console.error('Errore POST utenti:', error);
        res.status(500).json({ message: 'Errore durante la creazione dell\'utente' });
    }
});

// 3. PUT: Modifica un utente esistente
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { username, password, ruolo_id } = req.body;
    try {
        // Se l'admin ha inserito una nuova password, la cifriamo e aggiorniamo tutto
        if (password && password.trim() !== '') {
            const saltRounds = 10;
            const hash = await bcrypt.hash(password, saltRounds);
            await pool.query(
                'UPDATE utenti SET username = $1, password_hash = $2, ruolo_id = $3 WHERE id = $4',
                [username, hash, ruolo_id, id]
            );
        } else {
            // Se la password è vuota, aggiorniamo solo username e ruolo senza toccare la password vecchia
            await pool.query(
                'UPDATE utenti SET username = $1, ruolo_id = $2 WHERE id = $3',
                [username, ruolo_id, id]
            );
        }
        res.json({ message: 'Utente aggiornato con successo!' });
    } catch (error) {
        console.error('Errore PUT utenti:', error);
        res.status(500).json({ message: 'Errore durante la modifica dell\'utente' });
    }
});

// 4. DELETE: Elimina un utente
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    try {
        // Evitiamo che l'admin si cancelli da solo per sbaglio (opzionale ma sicuro)
        if (parseInt(id) === 1) {
            return res.status(400).json({ message: 'Non è possibile eliminare l\'amministratore principale' });
        }

        await pool.query('DELETE FROM utenti WHERE id = $1', [id]);
        res.json({ message: 'Utente eliminato con successo!' });
    } catch (error) {
        console.error('Errore DELETE utenti:', error);
        res.status(500).json({ message: 'Errore durante l\'eliminazione dell\'utente' });
    }
});

// Esportiamo il router per farlo usare a server.js
module.exports = router;