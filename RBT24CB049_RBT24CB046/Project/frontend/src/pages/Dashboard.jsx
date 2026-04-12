import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    LayoutDashboard, 
    Send, 
    History, 
    User, 
    CreditCard, 
    ArrowUpRight, 
    ArrowDownLeft, 
    LogOut, 
    ChevronRight,
    TrendingUp,
    RefreshCw,
    ShieldCheck,
    PieChart,
    Wallet
} from 'lucide-react';
import useStore from '../store/useStore';
import TransferModal from '../components/TransferModal';
import FDModal from '../components/FDModal';
import RDModal from '../components/RDModal';

export default function Dashboard() {
    const { user, fetchProfile, fetchTransactions, transactions, logout, investments, fetchInvestments } = useStore();
    const [isTransferModalOpen, setIsTransferModalOpen] = useState(false);
    const [isFDModalOpen, setIsFDModalOpen] = useState(false);
    const [isRDModalOpen, setIsRDModalOpen] = useState(false);
    const [isRefreshing, setIsRefreshing] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (!user) {
            navigate('/');
        } else {
            fetchProfile();
            fetchTransactions();
            fetchInvestments();
        }
    }, [navigate, user?._id]);

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    const handleRefresh = async () => {
        setIsRefreshing(true);
        await Promise.all([fetchProfile(), fetchTransactions(), fetchInvestments()]);
        setIsRefreshing(false);
    };

    if (!user) return null;

    return (
        <div className="min-h-screen bg-[#0f172a] text-slate-100 flex flex-col md:flex-row font-sans">
            {/* Sidebar (Desktop) */}
            <aside className="w-full md:w-64 glass md:border-r border-slate-800/50 p-6 flex flex-col items-center">
                <div className="flex items-center gap-3 mb-12">
                    <div className="p-2 bg-blue-600 rounded-lg shadow-lg shadow-blue-600/30">
                        <CreditCard className="w-5 h-5 text-white" />
                    </div>
                    <span className="text-xl font-bold tracking-tight">NexusBank</span>
                </div>

                <nav className="flex-1 w-full space-y-2">
                    <button className="flex items-center gap-3 w-full p-4 rounded-xl bg-blue-600 text-white shadow-lg shadow-blue-600/20">
                        <LayoutDashboard className="w-5 h-5" />
                        <span className="font-semibold">My Capital</span>
                    </button>
                    <button 
                        onClick={() => setIsTransferModalOpen(true)}
                        className="flex items-center gap-3 w-full p-4 rounded-xl text-slate-400 hover:text-white hover:bg-white/5 transition-all"
                    >
                        <Send className="w-5 h-5" />
                        <span className="font-medium">Payments</span>
                    </button>
                </nav>

                <button 
                    onClick={handleLogout}
                    className="mt-auto flex items-center gap-3 w-full p-4 rounded-xl text-rose-500 hover:bg-rose-500/10 transition-all font-semibold"
                >
                    <LogOut className="w-5 h-5" />
                    Secure Logout
                </button>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto p-6 md:p-10">
                <div className="max-w-6xl mx-auto space-y-10">
                    
                    {/* Header */}
                    <div className="flex items-center justify-between">
                        <div>
                            <h2 className="text-3xl font-black tracking-tight underline decoration-blue-600 underline-offset-8 decoration-4">Hi, {user.name.split(' ')[0]}</h2>
                            <p className="text-slate-500 mt-2 font-medium">Monitoring your institutional liquidity</p>
                        </div>
                        <div className="flex gap-4">
                             <button 
                                onClick={handleRefresh}
                                className={`p-4 rounded-2xl bg-white/5 hover:bg-white/10 transition-all border border-white/5 ${isRefreshing ? 'animate-spin border-blue-500' : ''}`}
                            >
                                <RefreshCw className={`w-5 h-5 ${isRefreshing ? 'text-blue-500' : 'text-slate-400'}`} />
                            </button>
                        </div>
                    </div>

                    {/* Quick Launch Actions */}
                    <div className="flex flex-wrap gap-4">
                        <button 
                            onClick={() => setIsFDModalOpen(true)}
                            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-2xl font-black text-sm uppercase tracking-widest shadow-xl shadow-blue-600/20 transition-all flex items-center gap-2"
                        >
                            <ShieldCheck className="w-4 h-4" /> Fixed Deposit
                        </button>
                        <button 
                            onClick={() => setIsRDModalOpen(true)}
                            className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-2xl font-black text-sm uppercase tracking-widest shadow-xl shadow-indigo-600/20 transition-all flex items-center gap-2"
                        >
                            <PieChart className="w-4 h-4" /> Recurring Deposit
                        </button>
                    </div>

                    {/* Stats Grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                        
                        {/* Balance Card */}
                        <motion.div 
                            initial={{ opacity: 0, scale: 0.98 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="relative overflow-hidden glass p-10 rounded-[3rem] lg:col-span-8 group border border-white/5 shadow-2xl"
                        >
                            <div className="absolute top-[-20%] right-[-10%] w-[50%] h-[150%] bg-blue-600/5 blur-[80px] transform rotate-12" />
                            <div className="relative z-10">
                                <div className="flex items-center justify-between mb-6">
                                    <div className="flex items-center gap-3">
                                        <Wallet className="w-5 h-5 text-blue-500" />
                                        <span className="text-slate-400 font-bold tracking-widest uppercase text-xs">Primary Vault</span>
                                    </div>
                                    <div className="p-2 bg-emerald-500/10 rounded-xl text-emerald-500 flex items-center gap-1 text-[10px] font-black uppercase tracking-tighter">
                                        <TrendingUp className="w-3 h-3" />
                                        <span>Active Growth</span>
                                    </div>
                                </div>
                                <h3 className="text-6xl font-black tracking-tighter mb-10 text-white drop-shadow-2xl">
                                    ${user.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                                </h3>
                                <div className="flex flex-wrap items-center gap-6">
                                    <button 
                                        onClick={() => setIsTransferModalOpen(true)}
                                        className="h-14 px-10 bg-white text-slate-900 rounded-[1.25rem] font-black text-sm uppercase tracking-widest flex items-center gap-2 hover:bg-blue-50 transition-all shadow-2xl shadow-blue-500/10 active:scale-95"
                                    >
                                        <Send className="w-4 h-4" /> Transfer
                                    </button>
                                    <div className="h-14 px-8 bg-white/5 rounded-[1.25rem] border border-white/5 flex items-center gap-4">
                                        <div className="p-2 bg-blue-500/10 rounded-lg">
                                            <ShieldCheck className="w-4 h-4 text-blue-400" />
                                        </div>
                                        <div className="flex flex-col">
                                            <span className="text-[10px] text-slate-500 font-black uppercase tracking-widest leading-none">Security ID</span>
                                            <span className="text-sm font-mono font-black text-slate-300">{user.accountNumber}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </motion.div>

                        {/* Summary Card */}
                        <motion.div 
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="bg-slate-900 border border-white/5 p-10 rounded-[3rem] lg:col-span-4 flex flex-col justify-between shadow-2xl"
                        >
                            <div>
                                <h4 className="text-slate-500 font-black uppercase tracking-widest text-[10px] mb-6">Financial Overview</h4>
                                <div className="space-y-6">
                                    <div>
                                        <div className="flex justify-between text-xs font-bold mb-2">
                                            <span className="text-slate-400">Fixed Deposits</span>
                                            <span className="text-blue-500">{investments.fds?.length || 0} Assets</span>
                                        </div>
                                        <div className="w-full bg-slate-800 h-1.5 rounded-full">
                                            <div className="bg-blue-500 h-full rounded-full" style={{ width: '45%' }} />
                                        </div>
                                    </div>
                                    <div>
                                        <div className="flex justify-between text-xs font-bold mb-2">
                                            <span className="text-slate-400">Recurring Deposits</span>
                                            <span className="text-indigo-500">{investments.rds?.length || 0} Assets</span>
                                        </div>
                                        <div className="w-full bg-slate-800 h-1.5 rounded-full">
                                            <div className="bg-indigo-500 h-full rounded-full" style={{ width: '65%' }} />
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <button className="w-full h-12 mt-8 rounded-2xl bg-white/5 border border-white/5 text-xs font-black uppercase tracking-widest hover:bg-white/10 transition-all text-slate-400">
                                View Full Portfolio
                            </button>
                        </motion.div>
                    </div>

                    {/* Active Investments Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* FD List */}
                        <section className="bg-slate-900/50 p-8 rounded-[2.5rem] border border-white/5">
                            <div className="flex items-center justify-between mb-8">
                                <h3 className="text-lg font-black uppercase tracking-widest text-slate-300">Fixed Deposits</h3>
                                <div className="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center">
                                    <ShieldCheck className="w-4 h-4 text-blue-500" />
                                </div>
                            </div>
                            <div className="space-y-4">
                                {investments.fds?.length > 0 ? investments.fds.map(fd => (
                                    <div key={fd._id} className="p-4 bg-white/[0.03] border border-white/5 rounded-2xl">
                                        <div className="flex justify-between mb-2">
                                            <span className="font-black text-white text-lg">${fd.amount.toLocaleString()}</span>
                                            <span className="text-[10px] bg-blue-600/10 text-blue-500 px-2 py-1 rounded font-black tracking-widest uppercase">Active</span>
                                        </div>
                                        <div className="flex justify-between text-[10px] text-slate-500 font-bold">
                                            <span>Maturity: {new Date(fd.maturityDate).toLocaleDateString()}</span>
                                            <span className="text-emerald-500">+{fd.interestRate}% Interest</span>
                                        </div>
                                    </div>
                                )) : <p className="text-slate-600 text-sm italic">No active Fixed Deposits.</p>}
                            </div>
                        </section>

                        {/* RD List */}
                        <section className="bg-slate-900/50 p-8 rounded-[2.5rem] border border-white/5">
                             <div className="flex items-center justify-between mb-8">
                                <h3 className="text-lg font-black uppercase tracking-widest text-slate-300">Recurring Deposits</h3>
                                <div className="w-8 h-8 rounded-full bg-indigo-500/10 flex items-center justify-center">
                                    <PieChart className="w-4 h-4 text-indigo-500" />
                                </div>
                            </div>
                            <div className="space-y-4">
                                {investments.rds?.length > 0 ? investments.rds.map(rd => (
                                    <div key={rd._id} className="p-4 bg-white/[0.03] border border-white/5 rounded-2xl">
                                        <div className="flex justify-between mb-2">
                                            <span className="font-black text-white text-lg">${rd.monthlyDeposit}/mo</span>
                                            <span className="text-[10px] bg-indigo-600/10 text-indigo-500 px-2 py-1 rounded font-black tracking-widest uppercase">75% Paid</span>
                                        </div>
                                        <div className="w-full bg-slate-800 h-1.5 rounded-full mb-3 overflow-hidden">
                                            <div className="bg-indigo-500 h-full rounded-full" style={{ width: '75%' }} />
                                        </div>
                                        <div className="flex justify-between text-[10px] text-slate-500 font-bold">
                                            <span>Est. Maturity: ${rd.maturityAmount.toLocaleString()}</span>
                                            <span className="text-emerald-500">{new Date(rd.maturityDate).toLocaleDateString()}</span>
                                        </div>
                                    </div>
                                )) : <p className="text-slate-600 text-sm italic">No active Recurring Deposits.</p>}
                            </div>
                        </section>
                    </div>

                    {/* Transactions Table */}
                    <div className="bg-slate-900 border border-white/5 overflow-hidden rounded-[2.5rem] shadow-2xl">
                        <div className="p-8 border-b border-white/5 flex items-center justify-between">
                            <h3 className="text-lg font-black uppercase tracking-widest text-slate-300 flex items-center gap-3">
                                <History className="w-5 h-5 text-blue-500" /> Recent Activity
                            </h3>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead className="bg-white/5 text-[10px] font-black uppercase tracking-widest text-slate-500">
                                    <tr>
                                        <th className="p-6">Execution Date</th>
                                        <th className="p-6">Transaction Note</th>
                                        <th className="p-6">Status Type</th>
                                        <th className="p-6 text-right">Settlement</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-white/5">
                                    {transactions.length === 0 ? (
                                        <tr><td colSpan="4" className="text-center py-20 text-slate-600 italic">No historical records found.</td></tr>
                                    ) : (
                                        transactions.slice().reverse().slice(0, 5).map((tx, idx) => (
                                            <tr key={tx._id || idx} className="hover:bg-white/[0.02] transition-colors group">
                                                <td className="p-6 text-xs font-bold text-slate-500">{new Date(tx.timestamp).toLocaleDateString()}</td>
                                                <td className="p-6">
                                                    <div className="font-bold text-slate-300">{tx.description}</div>
                                                </td>
                                                <td className="p-6 text-[10px] font-black tracking-widest uppercase">
                                                    <span className={tx.type === 'CREDIT' ? 'text-emerald-500' : 'text-rose-500'}>{tx.type}</span>
                                                </td>
                                                <td className={`p-6 text-right font-mono font-bold text-sm ${tx.type === 'CREDIT' ? 'text-emerald-500' : 'text-rose-500'}`}>
                                                    {tx.type === 'CREDIT' ? '+' : '-'}${tx.amount.toLocaleString()}
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>

                </div>
            </main>

            {/* Modals */}
            <TransferModal isOpen={isTransferModalOpen} onClose={() => setIsTransferModalOpen(false)} />
            <FDModal isOpen={isFDModalOpen} onClose={() => setIsFDModalOpen(false)} />
            <RDModal isOpen={isRDModalOpen} onClose={() => setIsRDModalOpen(false)} />
        </div>
    );
}
