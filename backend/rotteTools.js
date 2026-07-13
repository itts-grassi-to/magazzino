const express = require('express');
const router = express.Router();
const { Pool } = require('pg');

const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:postgres@db:5432/magazzino'
});

// ==========================================
// TOOL 1: RICERCA SCORTE E PRE-FILTRAGGIO
// ==========================================
router.get('/scorte', async (req, res) => {
    const { termine, id_categoria } = req.query;

    try {
        let querySql = `
            SELECT 
                p.id, p.sigla, p.descrizione, p.codice_a_barre, p.link, p.data_scadenza,
                c.descrizione AS categoria,
                COALESCE(SUM(CASE WHEN m.operazione = 'INGRESSO' THEN m.quantita ELSE 0 END), 0) -
                COALESCE(SUM(CASE WHEN m.operazione = 'USCITA' THEN m.quantita ELSE 0 END), 0) AS scorta_attuale
            FROM prodotto p
            LEFT JOIN categoria c ON p.id_categoria = c.id
            LEFT JOIN movimenti m ON p.id = m.id_prodotto
            WHERE 1=1
        `;

        const params = [];
        let paramIndex = 1;

        if (termine && termine.trim() !== '') {
            querySql += ` AND (p.sigla ILIKE $${paramIndex} OR p.descrizione ILIKE $${paramIndex} OR p.codice_a_barre ILIKE $${paramIndex})`;
            params.push(`%${termine.trim()}%`);
            paramIndex++;
        }

        if (id_categoria && id_categoria !== '') {
            querySql += ` AND p.id_categoria = $${paramIndex}`;
            params.push(parseInt(id_categoria));
            paramIndex++;
        }

        querySql += ` GROUP BY p.id, c.descrizione ORDER BY scorta_attuale DESC, p.sigla ASC`;

        const result = await pool.query(querySql, params);
        return res.json(result.rows);

    } catch (error) {
        console.error("Errore Tool Scorte:", error);
        return res.status(500).json({ message: "Errore nel calcolo delle giacenze." });
    }
});

// 🚀 DA QUI IN POI POTRAI AGGIUNGERE I NUOVI MODULI (TOOL 2, TOOL 3...) PER LA V2.0
// router.get('/scaduti', ...);

module.exports = router;