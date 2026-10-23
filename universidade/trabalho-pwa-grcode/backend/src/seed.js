// Importamos a biblioteca web-push instalada no package.json
const webpush = require('web-push');

const gerarChavesVapid = () => {
    console.log('🔑 --- GERADOR DE CREDENCIAIS WEB PUSH (VAPID) ---');
    console.log('Gerando chaves criptográficas seguras para o projeto...');
    
    // Gera o par de chaves usando o algoritmo padrão do protocolo push (VAPID)
    const chavesVapid = webpush.generateVAPIDKeys();
    
    console.log('\n======================================================');
    console.log('🟢 COPIE AS LINHAS ABAIXO E COLE NO SEU ARQUIVO .ENV:');
    console.log('======================================================\n');
    console.log(`VAPID_PUBLIC_KEY=${chavesVapid.publicKey}`);
    console.log(`VAPID_PRIVATE_KEY=${chavesVapid.privateKey}`);
    console.log('\n======================================================');
    console.log('⚠️ Guarde a Private Key em segredo e passe a Public Key para o Edgar!');
};

// Executa a função imediatamente ao chamar o arquivo
gerarChavesVapid();