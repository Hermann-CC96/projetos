const express = require('express');
const cors = require('cors');
const app = express();

// Importação das rotas
const authRoutes = require('./routes/authRoutes');
const qrRoutes = require('./routes/qrRoutes');
const pushRoutes = require('./routes/pushRoutes'); // <-- Nova importação


// Middlewares Globais
app.use(cors());
app.use(express.json());

// Registro dos Endpoints na API
app.use('/api/auth', authRoutes);
app.use('/api/qrcodes', qrRoutes);
app.use('/api/push', pushRoutes); // <-- Nova ativação

// Rota de Health Check
app.use('/api/status', (req, res) => {
    res.json({ 
        status: "Online", 
        mensagem: "API funcional. Rotas de Autenticação, QR-Codes e Push ativas." 
    });
});

module.exports = app;