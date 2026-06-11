const express = require('express');
const router = express.Router();
const { register, login, getMe, googleCallback } = require('../controllers/authController');
const { auth } = require('../middleware/auth');

router.post('/register', register);
router.post('/login', login);
router.post('/google', googleCallback);
router.get('/me', auth, getMe);

module.exports = router;