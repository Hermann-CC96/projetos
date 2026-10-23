const mongoose = require('mongoose');

// Define a estrutura da assinatura de push que guardaremos no banco
const PushSubscriptionSchema = new mongoose.Schema({
    // Vincula a assinatura ao cliente logado para sabermos de quem é o celular/navegador
    clienteId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Cliente',
        required: true
    },
    // URL gerada pelo navegador do cliente para envio das mensagens
    endpoint: {
        type: String,
        required: true,
        unique: true // Evita duplicar a mesma inscrição de aparelho no banco
    },
    // Chaves criptográficas do navegador do usuário
    keys: {
        p256dh: { type: String, required: true },
        auth: { type: String, required: true }
    },
    createdAt: {
        type: Date,
        default: Date.now
    }
});

module.exports = mongoose.model('PushSubscription', PushSubscriptionSchema);