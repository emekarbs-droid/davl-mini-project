const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const activityLogSchema = new mongoose.Schema({
    type: { type: String, required: true }, // 'DEBIT', 'CREDIT', 'TRANSFER'
    amount: { type: Number, required: true },
    description: { type: String, required: true },
    timestamp: { type: Date, default: Date.now }
});

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'Name is required']
    },
    email: {
        type: String,
        required: [true, 'Email is required'],
        unique: true,
        match: [
            /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
            'Please add a valid email'
        ]
    },
    password: {
        type: String,
        required: [true, 'Password is required'],
        minlength: 6,
        select: false
    },
    accountNumber: {
        type: String,
        required: true,
        unique: true,
        length: 10
    },
    balance: {
        type: Number,
        default: 1000.00 // Default opening balance
    },
    isAdmin: {
        type: Boolean,
        default: false
    },
    activityLog: [activityLogSchema]
}, {
    timestamps: true
});

// Hash password before saving
userSchema.pre('save', async function(next) {
    if (!this.isModified('password')) {
        next();
    }
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
});

// Match password method
userSchema.methods.matchPassword = async function(enteredPassword) {
    return await bcrypt.compare(enteredPassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
