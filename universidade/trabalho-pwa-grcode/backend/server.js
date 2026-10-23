// Carrega as variáveis do seu arquivo .env para a memória do Node.js
require('dotenv').config();

const app = require('./src/app');
const connectDB = require('./src/config/db');

// Define a porta usando o .env ou assume a 3000 como padrão de segurança
const PORT = process.env.PORT || 3000;

// Função assíncrona que gerencia a inicialização segura do sistema
const startServer = async () => {
    // 1º Passo: Aguarda o MongoDB conectar com sucesso
    await connectDB();

    // 2º Passo: Abre as portas de rede para começar a ouvir o aplicativo do Edgar
    app.listen(PORT, () => {
        console.log(`🚀 Servidor HTTP rodando perfeitamente na porta ${PORT}`);
        console.log(`📡 Pronto para testes locais em: http://localhost:${PORT}/api/status`);
    });
};

// Dá a partida no servidor
startServer();