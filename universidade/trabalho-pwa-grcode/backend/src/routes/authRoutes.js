const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

// Rota para cadastrar um novo cliente: POST /api/auth/registrar
router.post('/registrar', authController.registrar);

// Rota para fazer login: POST /api/auth/login
router.post('/login', authController.login);

module.exports = router;