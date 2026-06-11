const Job = require('../models/Job');

exports.getJobs = async (req, res) => {
  try {
    const {
      search,
      location,
      category,
      job_type,
      experience_level,
      work_mode,
      min_salary,
      max_salary,
      page = 1,
      limit = 10
    } = req.query;

    const query = { status: 'published' };

    if (search) {
      query.$text = { $search: search };
    }

    if (location) {
      query.location = { $regex: location, $options: 'i' };
    }

    if (category) {
      query.category = category;
    }

    if (job_type) {
      query.job_type = job_type;
    }

    if (experience_level) {
      query.experience_level = experience_level;
    }

    if (work_mode) {
      if (work_mode === 'remote') query.is_remote = true;
      if (work_mode === 'hybrid') query.is_hybrid = true;
      if (work_mode === 'onsite') query.is_onsite = true;
    }

    if (min_salary || max_salary) {
      query.salary_min = {};
      if (min_salary) query.salary_min.$gte = Number(min_salary);
      if (max_salary) query.salary_max = { $lte: Number(max_salary) };
    }

    const jobs = await Job.find(query)
      .populate('company', 'name logo')
      .sort({ createdAt: -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit);

    const count = await Job.countDocuments(query);

    res.json({
      jobs,
      totalPages: Math.ceil(count / limit),
      currentPage: page,
      total: count
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

exports.getJob = async (req, res) => {
  try {
    const job = await Job.findById(req.params.id)
      .populate('company', 'name logo description website')
      .populate('posted_by', 'name');

    if (!job) {
      return res.status(404).json({ message: 'Job not found' });
    }

    job.views_count += 1;
    await job.save();

    res.json(job);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

exports.createJob = async (req, res) => {
  try {
    const jobData = {
      ...req.body,
      posted_by: req.user.id
    };

    const job = await Job.create(jobData);
    res.status(201).json(job);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

exports.updateJob = async (req, res) => {
  try {
    const job = await Job.findById(req.params.id);

    if (!job) {
      return res.status(404).json({ message: 'Job not found' });
    }

    if (job.posted_by.toString() !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json({ message: 'Not authorized' });
    }

    const updatedJob = await Job.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }
    );

    res.json(updatedJob);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

exports.deleteJob = async (req, res) => {
  try {
    const job = await Job.findById(req.params.id);

    if (!job) {
      return res.status(404).json({ message: 'Job not found' });
    }

    if (job.posted_by.toString() !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json({ message: 'Not authorized' });
    }

    await job.deleteOne();
    res.json({ message: 'Job removed' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

exports.getCategories = async (req, res) => {
  try {
    const categories = await Job.distinct('category');
    res.json(categories);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

exports.getLocations = async (req, res) => {
  try {
    const locations = await Job.distinct('location');
    res.json(locations);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};