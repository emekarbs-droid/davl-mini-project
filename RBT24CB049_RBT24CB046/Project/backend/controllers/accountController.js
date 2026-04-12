const mongoose = require('mongoose');
const User = require('../models/userModel');
const Transaction = require('../models/transactionModel');

// @desc    Transfer funds
// @route   POST /api/accounts/transfer
// @access  Private
const transferFunds = async (req, res, next) => {
    try {
        const { recipientAccountNumber, amount } = req.body;
        const senderId = req.user._id;

        if (!recipientAccountNumber || !amount || amount <= 0) {
            res.status(400);
            throw new Error('Invalid transfer details');
        }

        const session = await mongoose.startSession();
        session.startTransaction();

        try {
            // Perform operations WITH transactions for ACID safety on Atlas
            const sender = await User.findById(senderId).session(session);
            if (!sender) throw new Error('Sender not found');
            
            if (sender.balance < amount) {
                throw new Error('Insufficient funds');
            }

            const recipient = await User.findOne({ accountNumber: recipientAccountNumber }).session(session);
            if (!recipient) {
                throw new Error('Recipient account not found');
            }

            if (sender.accountNumber === recipientAccountNumber) {
                throw new Error('Cannot transfer to yourself');
            }

            // Debit sender
            sender.balance -= Number(amount);
            sender.activityLog.push({
                type: 'DEBIT',
                amount,
                description: `Transferred to account: ${recipientAccountNumber}`
            });
            await sender.save({ session });

            // Credit recipient
            recipient.balance += Number(amount);
            recipient.activityLog.push({
                type: 'CREDIT',
                amount,
                description: `Received from account: ${sender.accountNumber}`
            });
            await recipient.save({ session });

            // Record global transaction for admin
            await Transaction.create([{
                sender: sender._id,
                senderAccountNumber: sender.accountNumber,
                recipient: recipient._id,
                recipientAccountNumber: recipient.accountNumber,
                amount: Number(amount)
            }], { session });

            await session.commitTransaction();
            session.endSession();

            res.status(200).json({
                message: 'Transfer successful',
                newBalance: sender.balance
            });

        } catch (error) {
            await session.abortTransaction();
            session.endSession();
            res.status(400);
            throw new Error(error.message);
        }
    } catch (err) {
        next(err);
    }
};

// @desc    Get account transactions (for current user)
// @route   GET /api/accounts/transactions
// @access  Private
const getTransactions = async (req, res, next) => {
    try {
        const user = await User.findById(req.user._id);
        if (user) {
            res.json(user.activityLog);
        } else {
            res.status(404);
            throw new Error('User not found');
        }
    } catch (error) {
        next(error);
    }
};

// @desc    Get all transactions (for admin)
// @route   GET /api/accounts/admin/transactions
// @access  Private/Admin
const getAllTransactions = async (req, res, next) => {
    try {
        const transactions = await Transaction.find()
            .populate('sender', 'name email')
            .populate('recipient', 'name email')
            .sort({ timestamp: -1 });
        res.json(transactions);
    } catch (error) {
        next(error);
    }
};

module.exports = {
    transferFunds,
    getTransactions,
    getAllTransactions
};
