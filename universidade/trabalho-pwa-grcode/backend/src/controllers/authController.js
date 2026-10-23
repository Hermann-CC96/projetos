const Cliente = require('../models/Cliente');
const PushSubscription = require('../models/PushSubscription'); // Importado
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const webpush = require('web-push'); // Importado

// Configuração do Web-Push usando as chaves do seu arquivo .env
if (process.env.VAPID_PUBLIC_KEY && process.env.VAPID_PRIVATE_KEY) {
    webpush.setVapidDetails(
        `mailto:${process.env.EMAIL_CONTATO || 'seu-email@dominio.com'}`,
        process.env.VAPID_PUBLIC_KEY,
        process.env.VAPID_PRIVATE_KEY
    );
}

// Lógica de Registro (Cadastro de Clientes)
exports.registrar = async (req, res) => {
    try {
        const { nome, email, cpf, senha } = req.body;

        // 1. Validação simples: verificar se o e-mail ou CPF já estão cadastrados
        const usuarioExiste = await Cliente.findOne({ $or: [{ email }, { cpf }] });
        if (usuarioExiste) {
            return res.status(400).json({ error: 'E-mail ou CPF já cadastrados no sistema.' });
        }

        // 2. Cria o novo cliente (o Model Cliente já vai hashear a senha automaticamente no pre-save)
        const novoCliente = await Cliente.create({ nome, email, cpf, senha });

        // 3. Retorna sucesso (omitindo a senha por segurança)
        return res.status(201).json({
            message: 'Cliente registrado com sucesso!',
            cliente: { id: novoCliente._id, nome: novoCliente.nome, email: novoCliente.email, cpf: novoCliente.cpf }
        });

    } catch (error) {
        return res.status(500).json({ error: 'Erro interno ao registrar cliente: ' + error.message });
    }
};

// Lógica de Login (Autenticação)
exports.login = async (req, res) => {
    try {
        const { email, senha } = req.body;

        // 1. Busca o cliente pelo e-mail
        const cliente = await Cliente.findOne({ email });
        if (!cliente) {
            return res.status(401).json({ error: 'E-mail ou senha inválidos.' });
        }

        // 2. Compara a senha digitada com a senha criptografada no banco
        const senhaValida = await bcrypt.compare(senha, cliente.senha);
        if (!senhaValida) {
            return res.status(401).json({ error: 'E-mail ou senha inválidos.' });
        }

        // 3. Gera o Token JWT contendo o ID do cliente dentro dele (payload)
        // Esse token expira em 7 dias (bom tempo para desenvolvimento acadêmico)
        const token = jwt.sign(
            { id: cliente._id }, 
            process.env.JWT_SECRET, 
            { expiresIn: '7d' }
        );

        // 4. Retorna o token para o front-end do Edgar salvar
        return res.status(200).json({
            message: 'Autenticação bem-sucedida!',
            token,
            cliente: { id: cliente._id, nome: cliente.nome, email: cliente.email }
        });

    } catch (error) {
        return res.status(500).json({ error: 'Erro interno ao fazer login: ' + error.message });
    }
};

/* ==========================================================================
   Novos métodos para controle do Web Push Notification
   ========================================================================== */

// Fornece a chave pública VAPID para o front-end criptografar a assinatura
exports.obterChavePublica = async (req, res) => {
    try {
        const publicKey = process.env.VAPID_PUBLIC_KEY;
        if (!publicKey) {
            return res.status(500).json({ error: 'Chave pública VAPID não configurada no servidor.' });
        }
        return res.status(200).json({ publicKey });
    } catch (error) {
        return res.status(500).json({ error: 'Erro ao obter chave pública: ' + error.message });
    }
};

// Recebe a assinatura do navegador e salva/atualiza no banco de dados
exports.salvarInscricaoPush = async (req, res) => {
    try {
        const { endpoint, keys } = req.body;
        const clienteId = req.usuarioId; // Obtido automaticamente do seu authMiddleware.js

        if (!endpoint || !keys || !keys.p256dh || !keys.auth) {
            return res.status(400).json({ error: 'Parâmetros de assinatura inválidos ou incompletos.' });
        }

        // Atualiza a assinatura se ela já existir para evitar duplicidade, ou cria uma nova
        const inscricao = await PushSubscription.findOneAndUpdate(
            { endpoint },
            { clienteId, endpoint, keys },
            { upsert: true, new: true }
        );

        return res.status(201).json({
            message: 'Inscrição de push registrada com sucesso!',
            inscricao
        });
    } catch (error) {
        return res.status(500).json({ error: 'Erro ao salvar inscrição de push: ' + error.message });
    }
};

// Envia uma notificação de teste ou aviso de QR Code lido para o cliente
exports.enviarNotificacaoSucesso = async (clienteId, titulo, mensagem) => {
    try {
        // Busca todas as inscrições registradas para este cliente (ele pode estar em mais de um dispositivo)
        const inscricoes = await PushSubscription.find({ clienteId });

        if (inscricoes.length === 0) return;

        const payload = JSON.stringify({
            title: titulo,
            body: mensagem
        });

        // Dispara para todas as assinaturas registradas daquele usuário
        const promessas = inscricoes.map(inscricao => {
            const pushSubscription = {
                endpoint: inscricao.endpoint,
                keys: {
                    p256dh: inscricao.keys.p256dh,
                    auth: inscricao.keys.auth
                }
            };
            return webpush.sendNotification(pushSubscription, payload)
                .catch(err => {
                    // Se o navegador rejeitar (assinatura expirou ou foi revogada), deleta do banco
                    if (err.statusCode === 410) {
                        return PushSubscription.deleteOne({ _id: inscricao._id });
                    }
                    console.error('Erro ao enviar push para uma das inscrições:', err);
                });
        });

        await Promise.all(promessas);
    } catch (error) {
        console.error('Erro geral ao processar envio de push:', error);
    }
};