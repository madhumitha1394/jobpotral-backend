const express = require('express');
const router = express.Router();
const {
  getProfile,
  updateProfile,
  saveJob,
  getSavedJobs,
  getAllUsers
} = require('../controllers/userController');
const { auth, authorize } = require('../middleware/auth');

router.get('/profile', auth, getProfile);
router.put('/profile', auth, updateProfile);
router.post('/save-job/:jobId', auth, saveJob);
router.get('/saved-jobs', auth, getSavedJobs);
router.get('/', auth, authorize('admin'), getAllUsers);

module.exports = router;