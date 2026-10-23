const API_URL = "http://localhost:3000/api";

// Função utilitária para pegar o token guardado no navegador
function obterToken() {
    return localStorage.getItem("token");
}

// 1. INTEGRAR CADASTRO (Necessita enviar o CPF conforme seu backend!)
async function cadastrar(nome, email, senha, cpf) {
    try {
        const resposta = await fetch(`${API_URL}/auth/registrar`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ nome, email, senha, cpf })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            return { sucesso: false, mensagem: dados.mensagem || "Erro ao cadastrar." };
        }

        return { sucesso: true };
    } catch (error) {
        console.error("Erro no cadastro:", error);
        return { sucesso: false, mensagem: "Não foi possível conectar ao servidor." };
    }
}

// 2. INTEGRAR LOGIN (Guarda o Token JWT e o nome do usuário)
async function login(email, senha) {
    try {
        const respuesta = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, senha })
        });

        const dados = await respuesta.json();

        if (!respuesta.ok) {
            return { sucesso: false, mensagem: dados.mensagem || "Credenciais inválidas." };
        }

        // Salva as credenciais essenciais de forma segura no navegador
        localStorage.setItem("token", dados.token);
        
        // Captura o nome de maneira flexível sem quebrar se o backend mandar um padrão diferente
        const nomeUsuario = dados.usuario?.nome || dados.user?.nome || "Usuário";
        localStorage.setItem("usuario", nomeUsuario);
        
        return { sucesso: true };
    } catch (error) {
        console.error("Erro no login:", error);
        return { sucesso: false, mensagem: "Não foi possível conectar ao servidor." };
    }
}

// 3. INTEGRAR SALVAR QR CODE (Envia para o banco autenticado via Middleware)
async function salvarQRCode(codigo) {
    try {
        const token = obterToken();
        if (!token) {
            return { sucesso: false, mensagem: "Usuário não autenticado." };
        }

        const resposta = await fetch(`${API_URL}/qrcodes`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ codigo })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
           return { sucesso: false, mensagem: dados.error || dados.mensagem || "Erro ao salvar código." }
        }

        return { sucesso: true };
    } catch (error) {
        console.error("Erro ao salvar QR Code:", error);
        return { sucesso: false, mensagem: "Erro de conexão com o servidor." };
    }
}

// 4. INTEGRAR LISTAGEM DE QR CODES (Busca direto do banco os dados do usuário logado)
async function listarQRCodes() {
    try {
        const token = obterToken();
        if (!token) return [];

        const resposta = await fetch(`${API_URL}/qrcodes`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!resposta.ok) return [];

        const dados = await resposta.json();
        console.log("Dados recebidos da API de QR Codes:", dados);

        // Mapeia diretamente o array 'codigos' que o backend envia
        if (dados && Array.isArray(dados.codigos)) {
            return dados.codigos.map(qr => qr.codigo || qr);
        }

        return [];
    } catch (error) {
        console.error("Erro ao listar QR Codes:", error);
        return [];
    }
}

// 5. OBTER CHAVE PÚBLICA VAPID (Busca do backend para registrar o Push)
async function obterChavePublicaVapid() {
    try {
        const resposta = await fetch(`${API_URL}/push/vapid-public-key`);
        const dados = await resposta.json();

        if (!resposta.ok) {
            return { sucesso: false, mensagem: dados.error || "Erro ao buscar chave pública VAPID." };
        }

        return { sucesso: true, publicKey: dados.publicKey };
    } catch (error) {
        console.error("Erro ao obter chave pública:", error);
        return { sucesso: false, mensagem: "Erro de conexão ao buscar chave VAPID." };
    }
}

// 6. ENVIAR INSCRIÇÃO DE PUSH (Salva o dispositivo do usuário logado no banco)
async function salvarInscricaoPush(assinatura) {
    try {
        const token = obterToken();
        if (!token) return { sucesso: false, mensagem: "Usuário não autenticado." };

        const resposta = await fetch(`${API_URL}/push/subscribe`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(assinatura) // Envia o objeto gerado pelo navegador
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            return { sucesso: false, mensagem: dados.error || "Erro ao salvar assinatura de notificações." };
        }

        return { sucesso: true };
    } catch (error) {
        console.error("Erro ao salvar inscrição de push:", error);
        return { sucesso: false, mensagem: "Erro de conexão ao salvar push." };
    }
}