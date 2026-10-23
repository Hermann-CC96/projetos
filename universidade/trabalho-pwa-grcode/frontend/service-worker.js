const CACHE_NAME = "promoqr-v1";

const urlsToCache = [
    "/",
    "/index.html",
    "/cadastro.html",
    "/home.html",
    "/scanner.html",
    "/qrcodes.html",
    "/css/style.css",
    "/js/api.js",
    "/js/login.js",
    "/js/cadastro.js",
    "/js/home.js",
    "/js/scanner.js",
    "/js/qrcodes.js"
];

// Instalação do Service Worker e Cache dos arquivos
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(urlsToCache);
            })
    );
});

// Interceptação das requisições para rodar offline
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
    );
});

/* ==========================================================================
   Integração do Sistema de Notificações Push
   ========================================================================== */

// 1. Escuta o disparo de notificações vindas do Back-end
self.addEventListener("push", event => {
    let dados = {
        titulo: "Novidade no PromoQR!",
        corpo: "Você tem uma nova atualização disponível.",
        icon: "images/icon-192.png",
        badge: "images/icon-192.png"
    };

    if (event.data) {
        try {
            // Tenta decodificar o payload JSON enviado pelo backend (Web-Push)
            const payload = event.data.json();
            dados.titulo = payload.title || dados.titulo;
            dados.corpo = payload.body || dados.corpo;
            if (payload.icon) dados.icon = payload.icon;
        } catch (e) {
            // Fallback caso o payload seja texto puro
            dados.corpo = event.data.text();
        }
    }

    const opcoes = {
        body: dados.corpo,
        icon: dados.icon,
        badge: dados.badge,
        vibrate: [100, 50, 100], // Padrão de vibração para celulares
        data: {
            url: "/qrcodes.html" // Rota para redirecionar no clique
        }
    };

    event.waitUntil(
        self.registration.showNotification(dados.titulo, opcoes)
    );
});

// 2. Controla o comportamento do clique na notificação
self.addEventListener("notificationclick", event => {
    event.notification.close(); // Fecha a notificação visualmente

    // Redireciona o usuário para o app
    const urlParaAbrir = new URL(event.notification.data?.url || "/", self.location.origin).href;

    event.waitUntil(
        clients.matchAll({ type: "window", includeUncontrolled: true })
            .then(windowClients => {
                // Se o app já estiver aberto em alguma aba, foca nela e redireciona
                for (let client of windowClients) {
                    if (client.url === urlParaAbrir && "focus" in client) {
                        return client.focus();
                    }
                }
                // Se o app estiver fechado, abre uma nova janela na rota configurada
                if (clients.openWindow) {
                    return clients.openWindow(urlParaAbrir);
                }
            })
    );
});