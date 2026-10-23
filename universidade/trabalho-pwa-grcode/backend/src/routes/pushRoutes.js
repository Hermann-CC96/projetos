const express = require('express');
const router = express.Router();
const pushController = require('../controllers/pushController');
const authMiddleware = require('../middlewares/authMiddleware');

// Rota pública: retorna a chave pública VAPID
router.get('/vapid-public-key', pushController.obterChavePublica);

// Rota protegida: salva a inscrição do push vinculada ao cliente logado
// GARANTA QUE O NOME AQUI SEJA EXATAMENTE "inscreverPush"
router.post('/subscribe', authMiddleware, pushController.inscreverPush);

module.exports = router;