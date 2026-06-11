const express = require('express');
const router = express.Router();
const Company = require('../models/Company');
const { auth, authorize } = require('../middleware/auth');

router.get('/', async (req, res) => {
  try {
    const companies = await Company.find().populate('created_by', 'name');
    res.json(companies);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

router.post('/', auth, authorize('employer', 'admin'), async (req, res) => {
  try {
    const company = await Company.create({
      ...req.body,
      created_by: req.user.id
    });
    res.status(201).json(company);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;