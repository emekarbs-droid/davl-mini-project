import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
    Users, 
    ArrowLeftRight, 
    LayoutDashboard, 
    LogOut, 
    Search,
    ShieldCheck,
    TrendingUp,
    RefreshCw,
    UserCircle,
    Calendar
} from 'lucide-react';
import useStore from '../store/useStore';

export default function AdminDashboard() {
    const { user, allUsers, allTransactions, fetchAllUsers, fetchAllTransactions, logout } = useStore();
    const [activeTab, setActiveTab] = useState('users');
    const [searchTerm, setSearchTerm] = useState('');
    const [isRefreshing, setIsRefreshing] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (!user || !user.isAdmin) {
            navigate('/');
            return;
        }
        handleRefresh();
    }, [user, navigate]);

    const handleRefresh = async () => {
        setIsRefreshing(true);
        await Promise.all([fetchAllUsers(), fetchAllTransactions()]);
        setIsRefreshing(false);
    };

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    const filteredUsers = allUsers.filter(u => 
        u.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
        u.accountNumber.includes(searchTerm)
    );

    const filteredTransactions = allTransactions.filter(tx => 
        tx.senderAccountNumber.includes(searchTerm) || 
        tx.recipientAccountNumber.includes(searchTerm) ||
        tx.sender?.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        tx.recipient?.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (!user || !user.isAdmin) return null;

    return (
        <div className="min-h-screen bg-[#020617] text-slate-100 flex flex-col md:flex-row font-sans">
            {/* Sidebar */}
            <aside className="w-full md:w-72 bg-slate-900/50 backdrop-blur-xl border-r border-white/5 p-8 flex flex-col">
                <div className="flex items-center gap-4 mb-12">
                    <div className="p-3 bg-indigo-600 rounded-2xl shadow-lg shadow-indigo-600/20">
                        <ShieldCheck className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold tracking-tight">Admin Portal</h1>
                        <p className="text-xs text-indigo-400 font-bold uppercase tracking-widest">NEXUSBANK SECURE</p>
                    </div>
                </div>

                <nav className="flex-1 space-y-2">
                    <button 
                        onClick={() => setActiveTab('users')}
                        className={`flex items-center gap-4 w-full p-4 rounded-2xl transition-all ${activeTab === 'users' ? 'bg-indigo-600 text-white shadow-xl shadow-indigo-600/20' : 'text-slate-400 hover:bg-white/5'}`}
                    >
                        <Users className="w-5 h-5" />
                        <span className="font-semibold">Users Management</span>
                    </button>
                    <button 
                        onClick={() => setActiveTab('transactions')}
                        className={`flex items-center gap-4 w-full p-4 rounded-2xl transition-all ${activeTab === 'transactions' ? 'bg-indigo-600 text-white shadow-xl shadow-indigo-600/20' : 'text-slate-400 hover:bg-white/5'}`}
                    >
                        <ArrowLeftRight className="w-5 h-5" />
                        <span className="font-semibold">Global Transactions</span>
                    </button>
                </nav>

                <div className="mt-auto pt-8 border-t border-white/5">
                    <div className="flex items-center gap-3 mb-6 p-2">
                        <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center">
                            <UserCircle className="w-6 h-6 text-slate-400" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-bold truncate">{user.fullName}</p>
                            <p className="text-xs text-slate-500 truncate">System Root</p>
                        </div>
                    </div>
                    <button 
                        onClick={handleLogout}
                        className="flex items-center gap-4 w-full p-4 rounded-2xl text-rose-500 hover:bg-rose-500/10 transition-all font-bold"
                    >
                        <LogOut className="w-5 h-5" />
                        Logout Session
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto p-8 md:p-12">
                <div className="max-w-6xl mx-auto space-y-8">
                    
                    {/* Top Bar */}
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                        <div>
                            <h2 className="text-3xl font-black tracking-tight">{activeTab === 'users' ? 'User Accounts' : 'Global History'}</h2>
                            <p className="text-slate-400 mt-1">Real-time overview of the banking ecosystem</p>
                        </div>

                        <div className="flex items-center gap-4">
                            <div className="relative">
                                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                                <input 
                                    type="text" 
                                    placeholder="Search details..." 
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="bg-slate-900 border-white/5 rounded-2xl pl-12 pr-6 h-12 w-full md:w-64 focus:ring-2 focus:ring-indigo-600 transition-all outline-none"
                                />
                            </div>
                            <button 
                                onClick={handleRefresh}
                                className={`p-3 rounded-2xl bg-slate-900 hover:bg-slate-800 transition-all border border-white/5 ${isRefreshing ? 'animate-spin' : ''}`}
                            >
                                <RefreshCw className="w-5 h-5 text-indigo-500" />
                            </button>
                        </div>
                    </div>

                    {/* Content Table */}
                    <motion.div 
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="bg-slate-900/50 backdrop-blur-md rounded-[2.5rem] border border-white/5 overflow-hidden shadow-2xl"
                    >
                        {activeTab === 'users' ? (
                            <div className="overflow-x-auto">
                                <table className="w-full text-left border-collapse">
                                    <thead>
                                        <tr className="bg-white/5">
                                            <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">Customer</th>
                                            <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">Account Number</th>
                                            <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">Balance</th>
                                            <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">Status</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-white/5">
                                        {filteredUsers.length > 0 ? filteredUsers.map((u) => (
                                            <tr key={u._id} className="hover:bg-white/[0.02] transition-colors group">
                                                <td className="p-6">
                                                    <div className="flex items-center gap-3">
                                                        <div className="w-10 h-10 rounded-xl bg-indigo-600/10 flex items-center justify-center text-indigo-500 font-bold">
                                                            {u.name.charAt(0)}
                                                        </div>
                                                        <div>
                                                            <div className="font-bold">{u.name}</div>
                                                            <div className="text-xs text-slate-500">{u.email}</div>
                                                        </div>
                                                    </div>
                                                </td>
                                                <td className="p-6 font-mono text-sm tracking-widest text-slate-400">{u.accountNumber}</td>
                                                <td className="p-6 font-bold text-emerald-500">${u.balance.toLocaleString()}</td>
                                                <td className="p-6">
                                                    <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-500 text-[10px] font-black uppercase tracking-widest">Active</span>
                                                </td>
                                            </tr>
                                        )) : (
                                            <tr>
                                                <td colSpan="4" className="p-20 text-center text-slate-500 italic">No users found matching your search.</td>
                                            </tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        ) : (
                            <div className="overflow-x-auto">
                                <table className="w-full text-left border-collapse">
                                    <thead>
                                        <tr className="bg-white/5">
                                            <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">Sender / Recipient</th>
                                            <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">Transaction Details</th>
                                            <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">Amount</th>
                                            <th className="p-6 text-xs font-bold text-slate-500 uppercase tracking-widest">Date & Time</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-white/5">
                                        {filteredTransactions.length > 0 ? filteredTransactions.map((tx) => (
                                            <tr key={tx._id} className="hover:bg-white/[0.02] transition-colors group">
                                                <td className="p-6">
                                                    <div className="flex items-center gap-6">
                                                        <div className="text-right">
                                                            <div className="font-bold text-slate-300">{tx.sender?.name || 'N/A'}</div>
                                                            <div className="text-[10px] font-mono text-slate-600">{tx.senderAccountNumber}</div>
                                                        </div>
                                                        <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center">
                                                            <ArrowLeftRight className="w-4 h-4 text-slate-500" />
                                                        </div>
                                                        <div>
                                                            <div className="font-bold text-slate-300">{tx.recipient?.name || 'N/A'}</div>
                                                            <div className="text-[10px] font-mono text-slate-600">{tx.recipientAccountNumber}</div>
                                                        </div>
                                                    </div>
                                                </td>
                                                <td className="p-6">
                                                    <div className="text-xs uppercase font-black text-indigo-500 tracking-tighter">Inter-Bank Wire</div>
                                                    <div className="text-[10px] text-slate-500 font-mono mt-1">{tx._id}</div>
                                                </td>
                                                <td className="p-6">
                                                    <div className="text-lg font-black text-white">${tx.amount.toLocaleString()}</div>
                                                </td>
                                                <td className="p-6">
                                                    <div className="flex items-center gap-2 text-slate-400">
                                                        <Calendar className="w-4 h-4" />
                                                        <div className="text-xs font-bold">
                                                            {new Date(tx.timestamp).toLocaleDateString()}
                                                            <span className="text-slate-600 ml-2">{new Date(tx.timestamp).toLocaleTimeString()}</span>
                                                        </div>
                                                    </div>
                                                </td>
                                            </tr>
                                        )) : (
                                            <tr>
                                                <td colSpan="4" className="p-20 text-center text-slate-500 italic">No transactions found matching your search.</td>
                                            </tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </motion.div>
                </div>
            </main>
        </div>
    );
}
