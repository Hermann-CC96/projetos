const mongoose = require('mongoose');

const QRCodeSchema = new mongoose.Schema({
    codigo: {
        type: String,
        required: [true, 'O valor do QR-Code é obrigatório'],
        unique: true, // REQUISITO: Cada código de embalagem só pode ser validado uma única vez
        trim: true
    },
    clienteId: {
        type: mongoose.Schema.Types.ObjectId, // Vinculação com o ID nativo do MongoDB
        ref: 'Cliente',
        required: [true, 'Todo QR-Code validado precisa pertencer a um cliente']
    },
    scannedAt: {
        type: Date,
        default: Date.now
    }
});

module.exports = mongoose.model('QRCode', QRCodeSchema);