const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');


const app = express();
app.use(cors());
app.use(express.json());

const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@db:5432/magazzino'
});

async function initDatabase() {
    try {
        await pool.query(`
            CREATE TABLE IF NOT EXISTS ruoli (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(50) UNIQUE NOT NULL
            );
        `);

        await pool.query(`
            CREATE TABLE IF NOT EXISTS utenti (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                ruolo_id INTEGER REFERENCES ruoli(id)
            );
        `);

        // Popoliamo i ruoli se non esistono
        const res = await pool.query('SELECT COUNT(*) FROM ruoli');
        if (parseInt(res.rows[0].count) === 0) {
            await pool.query(`INSERT INTO ruoli (id, nome) VALUES (1, 'OPERATORE'), (2, 'MANAGER'), (3, 'ADMIN')`);
            console.log('✅ Ruoli inizializzati.');
        }
        // Inizializziamo l'utente admin se non esiste
        const resUtenti = await pool.query('SELECT COUNT(*) FROM utenti');
        if (parseInt(resUtenti.rows[0].count) === 0) {
            // Generiamo l'hash cifrato per la parola 'password'
            const saltRounds = 10;
            const hash = await bcrypt.hash('password', saltRounds);

            // Inseriamo l'admin associandolo al ruolo_id 3 (ADMIN)
            await pool.query(
                'INSERT INTO utenti (username, password_hash, ruolo_id) VALUES ($1, $2, $3)',
                ['admin', hash, 3]
            );
            console.log('👤 Utente di test "admin" creato con successo!');
        }

        await pool.query(`
            CREATE TABLE IF NOT EXISTS asset_older (
                id SERIAL PRIMARY KEY,
                sigla VARCHAR(50) UNIQUE NOT NULL,
                descrizione VARCHAR(255)
            );
        `);
        await pool.query(`
            CREATE TABLE IF NOT EXISTS categoria (
                id SERIAL PRIMARY KEY,
                descrizione VARCHAR(100) NOT NULL
            );
        `);
        await pool.query(`
            CREATE TABLE IF NOT EXISTS prodotto (
                id SERIAL PRIMARY KEY,
                sigla VARCHAR(50) UNIQUE NOT NULL,
                descrizione VARCHAR(255)  default NULL,
                link VARCHAR(255) default NULL,
                codice_a_barre VARCHAR(100) UNIQUE,
                id_categoria INTEGER REFERENCES categoria(id) ON DELETE SET NULL,
                id_utente_creatore INTEGER REFERENCES utenti(id),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        `);
        await pool.query(`
            CREATE TABLE IF NOT EXISTS movimenti (
                id SERIAL PRIMARY KEY,
                id_prodotto INTEGER REFERENCES prodotto(id) ON DELETE CASCADE,
                id_utente INTEGER REFERENCES utenti(id), 
                id_asset_older INTEGER REFERENCES asset_older(id) ON DELETE SET NULL, -- <--- ECCO IL DOVE!
                quantita INTEGER NOT NULL CHECK (quantita > 0),
                operazione VARCHAR(10) NOT NULL CHECK (operazione IN ('INGRESSO', 'USCITA')),
                data_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        `);
        // --- POPOLAMENTO UTILI DATI DI TEST SE VUOTE ---
        const resAsset = await pool.query('SELECT COUNT(*) FROM asset_older');
        if (parseInt(resAsset.rows[0].count) === 0) {
            await pool.query(`
                INSERT INTO asset_older (sigla, descrizione) VALUES 
                ('CASSETTO_1', 'Scaffalatura principale - Settore A'),
                ('ARMADIO_01', 'Armadio blindato Hardware'),
                ('LAB_TEST', 'Laboratorio collaudi e riparazioni')
            `);
            console.log('📍 Luoghi di stoccaggio (Asset Older) inizializzati.');
        }
        const resCat = await pool.query('SELECT COUNT(*) FROM categoria');
        if (parseInt(resCat.rows[0].count) === 0) {
            await pool.query(`INSERT INTO categoria (descrizione) 
                VALUES ('Hardware'), ('Software'), ('Medicine'), ('Cancelleria')`);
            console.log('📦 Categorie di test inizializzate.');
        }
        console.log('✅ Database pronto.');
    } catch (err) {
        console.error('❌ Errore inizializzazione DB:', err);
    }
}

initDatabase();

// ROUTE DI LOGIN
app.post('/api/auth/login', async (req, res) => {
    const { username, password } = req.body;
    try {
        const query = `
            SELECT u.*, r.nome AS ruolo 
            FROM utenti u 
            JOIN ruoli r ON u.ruolo_id = r.id 
            WHERE u.username = $1
        `;
        const result = await pool.query(query, [username]);

        if (result.rows.length === 0) {
            return res.status(400).json({ message: 'Username o password errati' });
        }

        const utente = result.rows[0];
        const passwordCorretta = await bcrypt.compare(password, utente.password_hash);

        if (!passwordCorretta) {
            return res.status(400).json({ message: 'Username o password errati' });
        }

        const token = jwt.sign(
            { id: utente.id, ruolo: utente.ruolo },
            'chiave_segreta_magazzino_2026',
            { expiresIn: '24h' }
        );

        res.json({
            token,
            utente: { id: utente.id, username: utente.username, ruolo: utente.ruolo }
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Errore interno del server' });
    }
});

//***************************** GESTIONE UTENTI **************/
const rotteUtenti = require('./rotteUtenti');
app.use('/api/utenti', rotteUtenti);
//***************************** GESTIONE MOVIMENTI (NUOVO) **************/
const rotteMovimenti = require('./rotteMovimenti');
app.use('/api/magazzino', rotteMovimenti);
//***************************** GESTIONE ASSET OLDER  **************/
const rotteAsset = require('./rotteAsset');
app.use('/api/asset-manager', rotteAsset);
//***************************** GESTIONE TOOLS  **************/
const rotteTools = require('./rotteTools');
app.use('/api/tools', rotteTools);
//** FINE GESTIONE   **************/

app.listen(5000, () => {
    console.log('Server del magazzino avviato sulla porta 5000');
});