import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import DashboardPostLogin from './dashboardPostLogin'; // <--- ECCCO L'IMPORT DEL NUOVO FILE!

function App() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [user, setUser] = useState(null);
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await fetch('http://localhost:5000/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Errore durante il login');
            localStorage.setItem('token', data.token);
            setUser(data.utente);
        } catch (err) {
            setError(err.message);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setUser(null);
        setUsername('');
        setPassword('');
    };

    // Se l'utente non è loggato, mostra la form di accesso
    if (!user) {
        return (
            <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px', fontFamily: 'sans-serif' }}>
                <h2>🔒 Accesso Magazzino</h2>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <form onSubmit={handleLogin}>
                    <div style={{ marginBottom: '10px' }}>
                        <label>Username:</label><br />
                        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} style={{ width: '100%', padding: '8px' }} required />
                    </div>
                    <div style={{ marginBottom: '20px' }}>
                        <label>Password:</label><br />
                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: '100%', padding: '8px' }} required />
                    </div>
                    <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007BFF', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                        Entra
                    </button>
                </form>
            </div>
        );
    }

    // SE L'UTENTE È LOGGATO: Richiama il componente dal file esterno!
    return (
        <DashboardPostLogin utente={user} onLogout={handleLogout} />
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);