const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const ClienteSchema = new mongoose.Schema({
    nome: {
        type: String,
        required: [true, 'O nome do cliente é obrigatório']
    },
    email: {
        type: String,
        required: [true, 'O e-mail é obrigatório'],
        unique: true, // Impedir cadastros duplicados com o mesmo e-mail
        lowercase: true, // Converte para minúsculo antes de salvar
        trim: true
    },
    cpf: {
        type: String,
        required: [true, 'O CPF é obrigatório'],
        unique: true, // REQUISITO ADICIONADO: Cada cliente deve possuir um CPF único no sistema
        trim: true
    },
    senha: {
        type: String,
        required: [true, 'A senha é obrigatória']
    },
    criadoEm: {
        type: Date,
        default: Date.now // Registra o momento exato do cadastro automaticamente
    }
});

// Middleware "pre-save": Executa lógica AUTOMATICAMENTE antes de salvar o documento no banco
ClienteSchema.pre('save', async function (next) {
    // Se a senha não foi modificada, pula a criptografia
    if (!this.isModified('senha')) return next();

    try {
        // Gera um "sal" (salt) para fortalecer a criptografia
        const salt = await bcrypt.genSalt(10);
        // Transforma a senha limpa em um hash seguro
        this.senha = await bcrypt.hash(this.senha, salt);
        next();
    } catch (error) {
        next(error);
    }
});

module.exports = mongoose.model('Cliente', ClienteSchema);