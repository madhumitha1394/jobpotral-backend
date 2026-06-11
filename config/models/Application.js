const mongoose = require('mongoose');

const applicationSchema = new mongoose.Schema({
  job: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Job',
    required: true
  },
  applicant: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  resume: {
    type: String,
    required: true
  },
  cover_letter: {
    type: String,
    default: ''
  },
  status: {
    type: String,
    enum: ['applied', 'screening', 'interview', 'offer', 'rejected', 'withdrawn'],
    default: 'applied'
  },
  answers: [{
    question: String,
    answer: String
  }]
}, {
  timestamps: true
});

applicationSchema.index({ job: 1, applicant: 1 }, { unique: true });

module.exports = mongoose.model('Application', applicationSchema);