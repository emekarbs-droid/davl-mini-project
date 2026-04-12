const express = require('express');
const router = express.Router();
const { transferFunds, getTransactions, getAllTransactions } = require('../controllers/accountController');
const { createFixedDeposit, createRecurringDeposit, getMyInvestments } = require('../controllers/investmentController');
const { protect, admin } = require('../middleware/authMiddleware');

router.post('/transfer', protect, transferFunds);
router.get('/transactions', protect, getTransactions);
router.get('/admin/transactions', protect, admin, getAllTransactions);

// Custom Investment Routes (FD/RD)
router.post('/invest/fd', protect, createFixedDeposit);
router.post('/invest/rd', protect, createRecurringDeposit);
router.get('/investments', protect, getMyInvestments);

module.exports = router;
