const express = require('express');
const router = express.Router();
const {
  applyForJob,
  getMyApplications,
  getJobApplications,
  updateApplicationStatus,
  withdrawApplication
} = require('../controllers/applicationController');
const { auth } = require('../middleware/auth');

router.post('/', auth, applyForJob);
router.get('/my', auth, getMyApplications);
router.get('/job/:jobId', auth, getJobApplications);
router.put('/:id/status', auth, updateApplicationStatus);
router.put('/:id/withdraw', auth, withdrawApplication);

module.exports = router;