const mongoose = require('mongoose');
const User = require('../models/userModel');
const FixedDeposit = require('../models/fixedDepositModel');
const RecurringDeposit = require('../models/recurringDepositModel');

// @desc    Create a Fixed Deposit
// @route   POST /api/accounts/invest/fd
// @access  Private
const createFixedDeposit = async (req, res, next) => {
    const session = await mongoose.startSession();
    session.startTransaction();

    try {
        const { amount, tenureMonths } = req.body;
        const user = await User.findById(req.user._id).session(session);

        if (user.balance < Number(amount)) {
            res.status(400);
            throw new Error('Insufficient balance to open FD');
        }

        const r = 0.065; // 6.5% interest
        const n = 12; // Monthly compounding
        const t = tenureMonths / 12; // years
        const maturityAmount = Number(amount) * Math.pow(1 + r/n, n * t);

        const maturityDate = new Date();
        maturityDate.setMonth(maturityDate.getMonth() + Number(tenureMonths));

        const fd = await FixedDeposit.create([{
            user: user._id,
            amount,
            interestRate: r * 100,
            tenureMonths,
            maturityAmount: Math.round(maturityAmount * 100) / 100,
            maturityDate
        }], { session });

        // Deduct from balance
        user.balance -= Number(amount);
        user.activityLog.push({
            type: 'DEBIT',
            amount,
            description: `Opened Fixed Deposit: ${fd[0]._id}`
        });
        await user.save({ session });

        await session.commitTransaction();
        session.endSession();

        res.status(201).json(fd[0]);

    } catch (error) {
        await session.abortTransaction();
        session.endSession();
        next(error);
    }
};

// @desc    Create a Recurring Deposit
// @route   POST /api/accounts/invest/rd
// @access  Private
const createRecurringDeposit = async (req, res, next) => {
    const session = await mongoose.startSession();
    session.startTransaction();

    try {
        const { monthlyDeposit, tenureMonths } = req.body;
        const user = await User.findById(req.user._id).session(session);

        if (user.balance < Number(monthlyDeposit)) {
            res.status(400);
            throw new Error('Insufficient balance to open RD (minimum 1st installment)');
        }

        const r = 0.072; // 7.2% interest
        // Simplified RD maturity calculation (Approximate for 1st installment growth)
        // In a real app, RD maturity = Sum of all future monthly installments' compounding
        // For this DBMS project, we estimate at creation
        const totalInvestment = Number(monthlyDeposit) * Number(tenureMonths);
        const maturityAmount = totalInvestment * (1 + (r * Number(tenureMonths) / 12));

        const maturityDate = new Date();
        maturityDate.setMonth(maturityDate.getMonth() + Number(tenureMonths));

        const rd = await RecurringDeposit.create([{
            user: user._id,
            monthlyDeposit,
            tenureMonths,
            totalDeposited: monthlyDeposit,
            maturityAmount: Math.round(maturityAmount * 100) / 100,
            maturityDate
        }], { session });

        // Deduct 1st installment
        user.balance -= Number(monthlyDeposit);
        user.activityLog.push({
            type: 'DEBIT',
            amount: monthlyDeposit,
            description: `Opened RD & Paid 1st Installment: ${rd[0]._id}`
        });
        await user.save({ session });

        await session.commitTransaction();
        session.endSession();

        res.status(201).json(rd[0]);

    } catch (error) {
        await session.abortTransaction();
        session.endSession();
        next(error);
    }
};

// @desc    Get user investments
// @route   GET /api/accounts/investments
// @access  Private
const getMyInvestments = async (req, res, next) => {
    try {
        const fds = await FixedDeposit.find({ user: req.user._id });
        const rds = await RecurringDeposit.find({ user: req.user._id });
        res.json({ fds, rds });
    } catch (error) {
        next(error);
    }
};

module.exports = {
    createFixedDeposit,
    createRecurringDeposit,
    getMyInvestments
};
