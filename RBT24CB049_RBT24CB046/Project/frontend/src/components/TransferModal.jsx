import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Send, CreditCard, DollarSign, Loader2, CheckCircle2 } from 'lucide-react';
import useStore from '../store/useStore';

export default function TransferModal({ isOpen, onClose }) {
    const [step, setStep] = useState(1); // 1: Form, 2: Success
    const [recipient, setRecipient] = useState('');
    const [amount, setAmount] = useState('');
    const [localError, setLocalError] = useState(null);
    const { user, transferFunds, loading, error, clearError } = useStore();

    const handleTransfer = async (e) => {
        e.preventDefault();
        setLocalError(null);
        clearError();

        // Validation
        const amountNum = parseFloat(amount);
        if (isNaN(amountNum) || amountNum <= 0) {
            setLocalError('Please enter a valid positive amount');
            return;
        }

        if (amountNum > user.balance) {
            setLocalError('Insufficient funds for this transaction');
            return;
        }

        if (recipient.length !== 10) {
            setLocalError('Account number must be exactly 10 digits');
            return;
        }

        if (recipient === user.accountNumber) {
            setLocalError('Cannot transfer funds to your own account');
            return;
        }

        try {
            await transferFunds(recipient, amountNum);
            setStep(2);
            setTimeout(() => {
                setStep(1);
                setRecipient('');
                setAmount('');
                onClose();
            }, 3000);
        } catch (err) {
            // Error is handled by global store
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md">
            <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="glass w-full max-w-md rounded-3xl overflow-hidden relative shadow-2xl"
            >
                {/* Header */}
                <div className="p-6 border-b border-white/5 flex items-center justify-between">
                    <h3 className="text-xl font-bold">Transfer Funds</h3>
                    <button onClick={onClose} className="p-1 hover:bg-white/10 rounded-full transition-colors">
                        <X className="w-6 h-6 text-slate-400" />
                    </button>
                </div>

                <div className="p-8">
                    <AnimatePresence mode="wait">
                        {step === 1 ? (
                            <motion.form 
                                key="form"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 20 }}
                                onSubmit={handleTransfer} 
                                className="space-y-6"
                            >
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-slate-400">Recipient Account Number</label>
                                    <div className="relative">
                                        <CreditCard className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                                        <input 
                                            type="text"
                                            placeholder="10-digit number"
                                            className="w-full pl-10 h-12"
                                            value={recipient}
                                            onChange={(e) => setRecipient(e.target.value.replace(/\D/g, '').slice(0, 10))}
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-slate-400">Amount (USD)</label>
                                    <div className="relative">
                                        <DollarSign className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                                        <input 
                                            type="number"
                                            step="0.01"
                                            placeholder="0.00"
                                            className="w-full pl-10 h-12"
                                            value={amount}
                                            onChange={(e) => setAmount(e.target.value)}
                                            required
                                        />
                                    </div>
                                    <div className="flex justify-between px-1">
                                        <span className="text-xs text-slate-500">Available: ${user.balance.toLocaleString()}</span>
                                        <button 
                                            type="button"
                                            onClick={() => setAmount(user.balance.toString())}
                                            className="text-xs text-blue-500 font-bold hover:underline"
                                        >
                                            Max
                                        </button>
                                    </div>
                                </div>

                                {(localError || error) && (
                                    <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-500 text-sm">
                                        {localError || error}
                                    </div>
                                )}

                                <button 
                                    type="submit" 
                                    disabled={loading}
                                    className="w-full h-14 bg-blue-600 hover:bg-blue-700 rounded-2xl font-bold flex items-center justify-center gap-2 transition-all shadow-xl shadow-blue-600/20 disabled:opacity-50"
                                >
                                    {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : (
                                        <>
                                            Confirm Transfer
                                            <Send className="w-5 h-5" />
                                        </>
                                    )}
                                </button>
                            </motion.form>
                        ) : (
                            <motion.div 
                                key="success"
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="flex flex-col items-center justify-center py-10 space-y-4 text-center"
                            >
                                <div className="w-20 h-20 bg-emerald-500/20 rounded-full flex items-center justify-center mb-4">
                                    <CheckCircle2 className="w-12 h-12 text-emerald-500" />
                                </div>
                                <h4 className="text-2xl font-bold">Transfer Successful!</h4>
                                <p className="text-slate-400">
                                    Your transfer of <span className="text-white font-bold">${parseFloat(amount).toLocaleString()}</span> to account <span className="text-white font-mono">{recipient}</span> has been processed.
                                </p>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </motion.div>
        </div>
    );
}
