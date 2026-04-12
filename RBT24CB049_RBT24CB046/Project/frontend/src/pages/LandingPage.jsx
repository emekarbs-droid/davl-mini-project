import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Landmark, Mail, Lock, User, ArrowRight, Loader2 } from 'lucide-react';
import useStore from '../store/useStore';

export default function LandingPage() {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: ''
    });

    const { login, register, user, loading, error, clearError } = useStore();
    const navigate = useNavigate();

    useEffect(() => {
        if (user) {
            navigate(user.isAdmin ? '/admin' : '/dashboard');
        }
        return () => clearError();
    }, [user, navigate, clearError]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (isLogin) {
            await login(formData.email, formData.password);
        } else {
            await register(formData.name, formData.email, formData.password);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#0f172a] p-4 relative overflow-hidden">
            {/* Background elements */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/10 blur-[120px]" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-600/10 blur-[120px]" />

            <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-12 items-center z-10">
                {/* Left Side: Branding */}
                <motion.div 
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6 }}
                    className="text-center lg:text-left"
                >
                    <div className="flex items-center justify-center lg:justify-start gap-3 mb-6">
                        <div className="p-3 bg-blue-600/20 rounded-2xl">
                            <Landmark className="w-8 h-8 text-blue-500" />
                        </div>
                        <span className="text-2xl font-bold tracking-tighter">NexusBank</span>
                    </div>
                    <h1 className="text-5xl lg:text-7xl font-bold leading-tight mb-6">
                        Banking <br /> 
                        <span className="gradient-text">Redefined</span>.
                    </h1>
                    <p className="text-slate-400 text-lg mb-8 max-w-md mx-auto lg:mx-0">
                        Modern financial infrastructure built for security, scale, and uncompromising speed.
                    </p>
                    
                    <div className="flex flex-wrap gap-4 justify-center lg:justify-start">
                        <div className="glass px-6 py-4 rounded-xl">
                            <div className="text-2xl font-bold">100%</div>
                            <div className="text-xs text-slate-500 uppercase tracking-widest">Secure</div>
                        </div>
                        <div className="glass px-6 py-4 rounded-xl">
                            <div className="text-2xl font-bold">Insta</div>
                            <div className="text-xs text-slate-500 uppercase tracking-widest">Transfers</div>
                        </div>
                    </div>
                </motion.div>

                {/* Right Side: Auth Form */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    className="glass p-8 lg:p-10 rounded-3xl w-full max-w-md mx-auto"
                >
                    <div className="flex gap-4 mb-8 p-1 bg-slate-900/50 rounded-xl">
                        <button 
                            onClick={() => setIsLogin(true)}
                            className={`flex-1 py-2 rounded-lg transition-all font-medium ${isLogin ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-500 hover:text-white'}`}
                        >
                            Login
                        </button>
                        <button 
                            onClick={() => setIsLogin(false)}
                            className={`flex-1 py-2 rounded-lg transition-all font-medium ${!isLogin ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-500 hover:text-white'}`}
                        >
                            Sign Up
                        </button>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <AnimatePresence mode="wait">
                            {!isLogin && (
                                <motion.div
                                    initial={{ opacity: 0, height: 0 }}
                                    animate={{ opacity: 1, height: 'auto' }}
                                    exit={{ opacity: 0, height: 0 }}
                                    className="space-y-2"
                                >
                                    <label className="text-sm font-medium text-slate-400">Full Name</label>
                                    <div className="relative">
                                        <User className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                                        <input 
                                            type="text" 
                                            placeholder="Enter your name"
                                            className="w-full pl-10"
                                            value={formData.name}
                                            onChange={e => setFormData({...formData, name: e.target.value})}
                                            required
                                        />
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-400">Email Address</label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                                <input 
                                    type="email" 
                                    placeholder="your@email.com"
                                    className="w-full pl-10"
                                    value={formData.email}
                                    onChange={e => setFormData({...formData, email: e.target.value})}
                                    required
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-400">Password</label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                                <input 
                                    type="password" 
                                    placeholder="••••••••"
                                    className="w-full pl-10"
                                    value={formData.password}
                                    onChange={e => setFormData({...formData, password: e.target.value})}
                                    required
                                    minLength={6}
                                />
                            </div>
                        </div>

                        {error && (
                            <motion.div 
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-500 text-sm"
                            >
                                {error}
                            </motion.div>
                        )}

                        <button 
                            type="submit" 
                            disabled={loading}
                            className="w-full py-4 bg-blue-600 hover:bg-blue-700 rounded-xl font-bold text-white shadow-xl shadow-blue-600/20 transition-all flex items-center justify-center gap-2 group disabled:opacity-50"
                        >
                            {loading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <>
                                    {isLogin ? 'Login to Portal' : 'Create Account'}
                                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                </>
                            )}
                        </button>
                    </form>

                    <p className="mt-8 text-center text-slate-500 text-sm">
                        By continuing, you agree to our terms of service and security policy.
                    </p>
                </motion.div>
            </div>
        </div>
    );
}
