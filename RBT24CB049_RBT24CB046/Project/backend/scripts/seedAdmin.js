const mongoose = require('mongoose');
const dotenv = require('dotenv');
const User = require('../models/userModel');

dotenv.config();

const seedAdmin = async () => {
    try {
        await mongoose.connect(process.env.MONGODB_URI);
        console.log('Connected to DB');

        const admin = await User.findOne({ $or: [{ email: 'root' }, { email: 'root@gmail.com' }] });
        if (admin) {
            console.log('Admin user found. Updating to root@gmail.com');
            admin.name = admin.name || admin.fullName || 'System Administrator';
            admin.email = 'root@gmail.com';
            admin.password = 'root@123';
            admin.isAdmin = true;
            admin.balance = admin.balance || admin.currentBalance || 99999999.00;
            await admin.save();
        } else {
            console.log('Creating Admin user "root@gmail.com"');
            await User.create({
                name: 'System Administrator',
                email: 'root@gmail.com',
                password: 'root@123',
                accountNumber: '0000000000',
                isAdmin: true,
                balance: 99999999.00
            });
        }

        console.log('Admin seeded successfully');
        process.exit();
    } catch (error) {
        console.error('Error seeding admin:', error);
        process.exit(1);
    }
};

seedAdmin();
