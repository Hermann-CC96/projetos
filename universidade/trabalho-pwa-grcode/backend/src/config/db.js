// Importamos a biblioteca Mongoose para interagir com o MongoDB
const mongoose = require('mongoose');

const connectDB = async () => {
    try {
        // Tentamos conectar ao banco usando a URI que você acabou de salvar no .env
        const conn = await mongoose.connect(process.env.MONGO_URI);
        
        // Log que vai aparecer no seu terminal confirmando o sucesso
        console.log(`🌿 MongoDB Conectado com sucesso: ${conn.connection.host}`);
    } catch (error) {
        // Se o seu MongoDB local estiver desligado, o código cai aqui
        console.error(`❌ Erro crítico na conexão com o MongoDB: ${error.message}`);
        
        // Derruba a aplicação imediatamente com código de falha (1)
        // Isso evita que o servidor fique rodando sem banco de dados
        process.exit(1);
    }
};

// Exportamos a função para que o inicializador mestre (server.js) possa usá-la
module.exports = connectDB;