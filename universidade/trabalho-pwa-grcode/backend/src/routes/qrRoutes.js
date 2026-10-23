const express = require('express');
const router = express.Router();
const qrController = require('../controllers/qrController');
const authMiddleware = require('../middlewares/authMiddleware');

// Passamos o authMiddleware antes do controlador. 
// A requisição só chega no controlador se o token for válido!

// Rota para cadastrar um código: POST /api/qrcodes
router.post('/', authMiddleware, qrController.cadastrarQRCode);

// Rota para listar os códigos do cliente logado: GET /api/qrcodes
router.get('/', authMiddleware, qrController.listarMeusQRCodes);

module.exports = router;