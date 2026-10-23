const QRCode = require('../models/QRCode');
const pushController = require('./pushController'); // Importa o controller de push recém-ajustado

// 1. Registrar um QR-Code escaneado: POST /api/qrcodes
exports.cadastrarQRCode = async (req, res) => {
    try {
        const { codigo } = req.body;
        
        // req.clienteId foi injetado de forma transparente pelo nosso authMiddleware
        const clienteId = req.clienteId; 

        // Validação simples de entrada de dados
        if (!codigo) {
            return res.status(400).json({ error: 'O código do QR-Code é obrigatório.' });
        }

        // Tenta criar o registro no MongoDB
        const novoQR = await QRCode.create({
            codigo,
            clienteId
        });

        // DISPARO DO PUSH: Envia uma notificação em tempo real para o dispositivo do cliente
        // Esta chamada é assíncrona, mas não bloqueia a resposta da requisição (não usamos await de propósito aqui)
        pushController.enviarNotificacaoSucesso(
            clienteId, 
            'Promoção Ativada! 🎉', 
            `O código "${codigo}" foi validado e acumulou em sua conta.`
        );

        return res.status(201).json({
            message: 'Código promocional cadastrado com sucesso!',
            qrCode: novoQR
        });

    } catch (error) {
        // Se cair aqui e o erro for o código 11000, significa que violou o índice "unique"
        if (error.code === 11000) {
            return res.status(400).json({ 
                error: 'Este QR-Code já foi cadastrado por outro participante!' 
            });
        }
        return res.status(500).json({ error: 'Erro ao cadastrar QR-Code: ' + error.message });
    }
};

// 2. Listar todos os QR-Codes do cliente logado: GET /api/qrcodes
exports.listarMeusQRCodes = async (req, res) => {
    try {
        const clienteId = req.clienteId;

        // Busca no banco apenas os códigos que possuem o clienteId correspondente
        // O .sort({ scannedAt: -1 }) traz os mais recentes primeiro (ótimo para a tela do Edgar)
        const meusCodigos = await QRCode.find({ clienteId }).sort({ scannedAt: -1 });

        return res.status(200).json({
            totalCadastrado: meusCodigos.length,
            codigos: meusCodigos
        });

    } catch (error) {
        return res.status(500).json({ error: 'Erro ao listar QR-Codes: ' + error.message });
    }
};