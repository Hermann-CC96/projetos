const jwt = require('jsonwebtoken');

module.exports = (req, res, next) => {
    // 1. Captura o cabeçalho de autorização da requisição HTTP
    const authHeader = req.headers.authorization;

    if (!authHeader) {
        return res.status(401).json({ error: 'Token de autenticação não fornecido.' });
    }

    // O formato padrão de envio do token é: "Bearer <TOKEN_AQUI>"
    // Dividimos a string pelo espaço para pegar apenas o token puro
    const partes = authHeader.split(' ');

    if (partes.length !== 2 || partes[0] !== 'Bearer') {
        return res.status(401).json({ error: 'Formato do token inválido. Use o padrão Bearer.' });
    }

    const token = partes[1];

    try {
        // 2. Verifica e decodifica o token usando a chave secreta do seu .env
        const decodificado = jwt.verify(token, process.env.JWT_SECRET);

        // 3. Injeta o ID do cliente dentro da própria requisição (req.clienteId)
        // Assim, os próximos controladores (como o de QR-Code) saberão exatamente quem está chamando
        req.clienteId = decodificado.id;

        // 4. Autoriza a requisição a continuar para a rota pretendida
        return next();

    } catch (error) {
        return res.status(401).json({ error: 'Token inválido ou expirado.' });
    }
};