// Carrega as variáveis do arquivo .env localizadas dentro da pasta backend
// Usamos o path.resolve para garantir que ele ache o .env não importa de onde você execute o comando
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../backend/.env') });

const mongoose = require('mongoose');
const webpush = require('web-push');

// REAPROVEITAMENTO: Ajustamos os caminhos (../backend/src/...) para apontar corretamente
// para a estrutura que você criou dentro da pasta backend
const QRCode = require('../backend/src/models/QRCode');
const PushSubscription = require('../backend/src/models/PushSubscription');
const connectDB = require('../backend/src/config/db');

// Configuração do Web-Push usando os dados do seu arquivo .env mapeado
webpush.setVapidDetails(
    process.env.PUSH_EMAIL,
    process.env.VAPID_PUBLIC_KEY,
    process.env.VAPID_PRIVATE_KEY
);

// Captura os argumentos do terminal (ex: node manda_msg <codigo> <mensagem>)
const codigoSorteado = process.argv[2];
const mensagemTexto = process.argv[3];

if (!codigoSorteado || !mensagemTexto) {
    console.error('❌ Erro: Formato inválido!');
    console.log('Use o comando assim: node manda_msg <codigo_qrcode> "sua mensagem aqui"');
    process.exit(1);
}

const dispararNotificacao = async () => {
    try {
        // Conecta ao banco usando a sua função do backend
        await connectDB();
        console.log(`\n🔍 Buscando o QR Code sorteado: "${codigoSorteado}"...`);

        // Procura o QR Code para descobrir quem é o cliente dono dele
        const qrEncontrado = await QRCode.findOne({ codigo: codigoSorteado });

        if (!qrEncontrado) {
            console.log(`❌ Código "${codigoSorteado}" não foi cadastrado por nenhum participante.`);
            process.exit(0);
        }

        console.log(`🎯 QR Code encontrado! Vinculado ao ID do Cliente: ${qrEncontrado.clienteId}`);

        // Busca a inscrição de push do navegador desse cliente específico
        const inscricao = await PushSubscription.findOne({ clienteId: qrEncontrado.clienteId });

        if (!inscricao) {
            console.log(`⚠️ O cliente cadastrou o código, mas não ativou as notificações no PWA.`);
            process.exit(0);
        }

        // Monta o payload (o corpo) da notificação
        const payload = JSON.stringify({
            title: '🎉 Promoção Biscoito X!',
            body: mensagemTexto,
            icon: '/assets/icon-192.png'
        });

        console.log('📡 Disparando notificação via Web-Push Protocol...');

        // Envia a notificação
        await webpush.sendNotification(
            {
                endpoint: inscricao.endpoint,
                keys: {
                    p256dh: inscricao.keys.p256dh,
                    auth: inscricao.keys.auth
                }
            },
            payload
        );

        console.log('🟢 Notificação enviada com sucesso para o dispositivo do ganhador!');

    } catch (error) {
        console.error('❌ Erro durante o processo de envio:', error.message);
    } finally {
        // Fecha a conexão de forma limpa
        await mongoose.connection.close();
        process.exit(0);
    }
};

dispararNotificacao();