const mongoose = require('mongoose');

const recurringDepositSchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    monthlyDeposit: {
        type: Number,
        required: true
    },
    interestRate: {
        type: Number,
        required: true,
        default: 7.2 // 7.2% interest for RD
    },
    tenureMonths: {
        type: Number,
        required: true
    },
    totalDeposited: {
        type: Number,
        required: true,
        default: 0
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

module.exports = mongoose.model('RecurringDeposit', recurringDepositSchema);
