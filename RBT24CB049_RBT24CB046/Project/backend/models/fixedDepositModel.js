const mongoose = require('mongoose');

const fixedDepositSchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    amount: {
        type: Number,
        required: true
    },
    interestRate: {
        type: Number,
        required: true,
        default: 6.5 // 6.5% interest
    },
    tenureMonths: {
        type: Number,
        required: true
    },
    maturityAmount: {
        type: Number,
        required: true
    },
    maturityDate: {
        type: Date,
        required: true
    },
    status: {
        type: String,
        enum: ['ACTIVE', 'MATURED'],
        default: 'ACTIVE'
    }
}, {
    timestamps: true
});

module.exports = mongoose.model('FixedDeposit', fixedDepositSchema);
