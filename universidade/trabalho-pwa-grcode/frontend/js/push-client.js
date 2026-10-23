/**
 * Utilitário para converter a chave VAPID pública do formato Base64 do backend
 * para uma Array de Bytes (Uint8Array) que o navegador exige no registro do push.
 */
function urlBase64ToUint8Array(base64String) {
    const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, "+")
        .replace(/_/g, "/");

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

/**
 * Função principal que inicializa o processo de Push Notification.
 * É disparada de forma segura nas páginas internas (home.html, qrcodes.html).
 */
async function inicializarPushNotification() {
    // 1. Verifica se o navegador suporta as APIs necessárias
    if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
        console.warn("Este navegador não suporta notificações Push.");
        return;
    }

    try {
        // 2. Solicita permissão de notificação se ainda não foi decidida
        let permissao = Notification.permission;
        if (permissao === "default") {
            permissao = await Notification.requestPermission();
        }

        if (permissao !== "granted") {
            console.warn("Permissão de notificação negada pelo usuário.");
            return;
        }

        // 3. Aguarda o Service Worker estar pronto
        const registro = await navigator.serviceWorker.ready;

        // 4. Verifica se já existe uma inscrição ativa neste navegador
        let assinatura = await registro.pushManager.getSubscription();

        // Se já existe, apenas garante que o back-end atualizou o vínculo
        if (assinatura) {
            console.log("Usuário já assina as notificações localmente.");
            await salvarInscricaoPush(assinatura);
            return;
        }

        // 5. Se não existe assinatura, busca a chave pública VAPID do servidor
        const resultadoChave = await obterChavePublicaVapid();
        if (!resultadoChave.sucesso || !resultadoChave.publicKey) {
            console.error("Falha ao obter a chave pública VAPID:", resultadoChave.mensagem);
            return;
        }

        // 6. Prepara a chave pública e registra o navegador no servidor de Push do navegador (Google/Mozilla/etc)
        const chaveConvertida = urlBase64ToUint8Array(resultadoChave.publicKey);
        
        assinatura = await registro.pushManager.subscribe({
            userVisibleOnly: true, // Obrigatório por segurança (toda mensagem recebida deve gerar um alerta visual)
            applicationServerKey: chaveConvertida
        });

        console.log("Nova assinatura gerada com sucesso para este dispositivo.");

        // 7. Envia o payload da assinatura gerada para o MongoDB via API
        const envioServidor = await salvarInscricaoPush(assinatura);
        if (envioServidor.sucesso) {
            console.log("Dispositivo vinculado com sucesso ao usuário no banco de dados.");
        } else {
            console.error("Erro ao registrar dispositivo no banco:", envioServidor.mensagem);
        }

    } catch (error) {
        console.error("Erro durante o fluxo de inicialização do Push:", error);
    }
}