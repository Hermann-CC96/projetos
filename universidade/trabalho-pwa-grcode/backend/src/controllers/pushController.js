const PushSubscription = require('../models/PushSubscription');
const webpush = require('web-push');

// Configuração global do Web-Push usando as chaves VAPID do arquivo .env
if (process.env.VAPID_PUBLIC_KEY && process.env.VAPID_PRIVATE_KEY) {
    webpush.setVapidDetails(
        `mailto:${process.env.EMAIL_CONTATO || 'seu-email@dominio.com'}`,
        process.env.VAPID_PUBLIC_KEY,
        process.env.VAPID_PRIVATE_KEY
    );
}

// 1. Retorna a chave pública para o Edgar poder registrar o Service Worker no front
exports.obterChavePublica = (req, res) => {
    const publicKey = process.env.VAPID_PUBLIC_KEY;
    
    if (!publicKey) {
        return res.status(500).json({ error: 'Chave pública VAPID não configurada no servidor.' });
    }
    
    return res.status(200).json({ publicKey });
};

// 2. Recebe a assinatura do front-end e salva associada ao cliente logado
exports.inscreverPush = async (req, res) => {
    try {
        const { endpoint, keys } = req.body;
        const clienteId = req.clienteId; // Injetado de forma transparente pelo seu authMiddleware

        // Validação simples dos dados do push
        if (!endpoint || !keys || !keys.p256dh || !keys.auth) {
            return res.status(400).json({ error: 'Dados da assinatura de push incompletos.' });
        }

        // Se o mesmo navegador já se inscreveu antes, apenas atualiza para não duplicar
        const assinaturaExistente = await PushSubscription.findOneAndUpdate(
            { endpoint },
            { clienteId, keys, createdAt: new Date() },
            { upsert: true, new: true } // Se não existir, o upsert cria um novo!
        );

        return res.status(201).json({
            message: 'Dispositivo inscrito nas notificações com sucesso!',
            subscription: assinaturaExistente
        });

    } catch (error) {
        return res.status(500).json({ error: 'Erro ao salvar inscrição de push: ' + error.message });
    }
};

// 3. Método utilitário para enviar notificações aos dispositivos de um cliente específico
exports.enviarNotificacaoSucesso = async (clienteId, titulo, mensagem) => {
    try {
        // Busca todas as inscrições (dispositivos) registradas para este cliente específico
        const inscricoes = await PushSubscription.find({ clienteId });

        if (inscricoes.length === 0) return;

        const payload = JSON.stringify({
            title: titulo,
            body: mensagem
        });

        // Dispara o envio paralelo para cada dispositivo cadastrado
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
                    // Se o servidor de push retornar 410, a assinatura expirou ou o usuário desativou.
                    // Nesse caso, limpamos o registro inválido do banco automaticamente.
                    if (err.statusCode === 410) {
                        return PushSubscription.deleteOne({ _id: inscricao._id });
                    }
                    console.error('Erro ao processar envio para um dispositivo:', err);
                });
        });

        await Promise.all(promessas);
    } catch (error) {
        console.error('Erro ao disparar notificações de sucesso:', error);
    }
};