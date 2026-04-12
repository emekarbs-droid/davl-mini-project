import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Calendar, Download, RefreshCcw, AlertCircle, Loader2 } from 'lucide-react';
import useStore from '../store/useStore';

export default function RDModal({ isOpen, onClose }) {
    const [monthlyDeposit, setMonthlyDeposit] = useState('');
    const [tenure, setTenure] = useState('12');
    const { createRD, loading, error, clearError } = useStore();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await createRD(monthlyDeposit, tenure);
            onClose();
            setMonthlyDeposit('');
        } catch (err) {
            // Error is handled in store
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-[#020617]/80 backdrop-blur-sm">
            <motion.div 
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 20 }}
                className="bg-slate-900 border border-white/10 rounded-[2.5rem] w-full max-w-lg p-8 shadow-2xl overflow-hidden relative"
            >
                {/* Header */}
                <div className="flex justify-between items-center mb-8">
                    <div className="flex items-center gap-3">
                        <div className="p-3 bg-indigo-600/10 rounded-2xl">
                            <RefreshCcw className="w-6 h-6 text-indigo-500" />
                        </div>
                        <h2 className="text-2xl font-bold">Open Recurring Deposit</h2>
                    </div>
                    <button onClick={onClose} className="p-2 hover:bg-white/5 rounded-full transition-colors"><X /></button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-slate-400">Monthly Contribution</label>
                        <div className="relative">
                            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 font-bold">$</span>
                            <input 
                                type="number" 
                                placeholder="0.00"
                                className="w-full pl-10 pr-6 py-4 bg-slate-800 border-white/5 rounded-2xl focus:ring-2 focus:ring-indigo-600 outline-none transition-all"
                                value={monthlyDeposit}
                                onChange={(e) => setMonthlyDeposit(e.target.value)}
                                required
                            />
                        </div>
                        <p className="text-[10px] text-slate-500 font-semibold uppercase tracking-widest pl-2">The first installment will be deducted immediately.</p>
                    </div>

                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-slate-400">Tenure (Months)</label>
                        <select 
                            className="w-full px-6 py-4 bg-slate-800 border-white/5 rounded-2xl focus:ring-2 focus:ring-indigo-600 outline-none transition-all appearance-none"
                            value={tenure}
                            onChange={(e) => setTenure(e.target.value)}
                        >
                            <option value="6">6 Months @ 6.8%</option>
                            <option value="12">12 Months @ 7.2%</option>
                            <option value="24">24 Months @ 7.8%</option>
                            <option value="36">36 Months @ 8.2%</option>
                        </select>
                    </div>

                    <div className="bg-indigo-600/5 p-4 rounded-2xl border border-indigo-600/10">
                        <div className="flex items-center gap-3 text-indigo-400 mb-2">
                            <Calendar className="w-4 h-4" />
                            <span className="text-xs font-black uppercase tracking-widest">Savings Builder</span>
                        </div>
                        <p className="text-sm text-slate-400 leading-relaxed italic">
                            Commit to consistent monthly savings and build a larger capital over time with high interest.
                        </p>
                    </div>

                    {error && (
                        <div className="p-4 bg-rose-500/10 border border-rose-500/20 rounded-2xl flex gap-3 text-rose-500 items-center">
                            <AlertCircle className="w-5 h-5 flex-shrink-0" />
                            <p className="text-sm font-bold">{error}</p>
                        </div>
                    )}

                    <button 
                        type="submit" 
                        disabled={loading}
                        className="w-full py-4 bg-indigo-600 hover:bg-indigo-700 rounded-2xl font-black text-white shadow-xl shadow-indigo-600/20 transition-all flex items-center justify-center gap-2 group disabled:opacity-50"
                    >
                        {loading ? <Loader2 className="animate-spin" /> : 'Confirm & Open RD'}
                    </button>
                </form>
            </motion.div>
        </div>
    );
}
