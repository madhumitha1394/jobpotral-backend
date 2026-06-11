const mongoose = require('mongoose');

const jobSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    trim: true
  },
  company: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Company',
    required: true
  },
  company_name: {
    type: String,
    required: true
  },
  location: {
    type: String,
    required: true
  },
  is_remote: {
    type: Boolean,
    default: false
  },
  is_hybrid: {
    type: Boolean,
    default: false
  },
  is_onsite: {
    type: Boolean,
    default: true
  },
  job_type: {
    type: String,
    enum: ['full_time', 'part_time', 'contract', 'freelance', 'internship'],
    default: 'full_time'
  },
  experience_level: {
    type: String,
    enum: ['entry', 'mid', 'senior', 'lead', 'executive'],
    default: 'mid'
  },
  category: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  requirements: [{
    type: String
  }],
  responsibilities: [{
    type: String
  }],
  salary_min: {
    type: Number,
    default: 0
  },
  salary_max: {
    type: Number,
    default: 0
  },
  salary_currency: {
    type: String,
    default: 'INR'
  },
  skills_required: [{
    type: String
  }],
  posted_by: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  status: {
    type: String,
    enum: ['draft', 'published', 'closed', 'expired'],
    default: 'published'
  },
  views_count: {
    type: Number,
    default: 0
  },
  applications_count: {
    type: Number,
    default: 0
  },
  expires_at: {
    type: Date,
    required: true
  }
}, {
  timestamps: true
});

jobSchema.index({ title: 'text', description: 'text', company_name: 'text' });
jobSchema.index({ category: 1 });
jobSchema.index({ location: 1 });
jobSchema.index({ job_type: 1 });
jobSchema.index({ experience_level: 1 });

module.exports = mongoose.model('Job', jobSchema);