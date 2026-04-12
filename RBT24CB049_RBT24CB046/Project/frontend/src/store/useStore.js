import { create } from 'zustand';
import api from '../api/api';

const useStore = create((set, get) => ({
    user: JSON.parse(localStorage.getItem('userInfo')) || null,
    loading: false,
    error: null,
    transactions: [],
    allUsers: [],
    allTransactions: [],
    investments: { fds: [], rds: [] },

    login: async (email, password) => {
        set({ loading: true, error: null });
        try {
            const { data } = await api.post('/users/login', { email, password });
            localStorage.setItem('userInfo', JSON.stringify(data));
            set({ user: data, loading: false });
        } catch (error) {
            set({ 
                error: error.response?.data?.message || error.message, 
                loading: false 
            });
        }
    },

    register: async (name, email, password) => {
        set({ loading: true, error: null });
        try {
            const { data } = await api.post('/users', { name, email, password });
            localStorage.setItem('userInfo', JSON.stringify(data));
            set({ user: data, loading: false });
        } catch (error) {
            set({ 
                error: error.response?.data?.message || error.message, 
                loading: false 
            });
        }
    },

    logout: () => {
        localStorage.removeItem('userInfo');
        set({ user: null, transactions: [], investments: { fds: [], rds: [] } });
    },

    fetchProfile: async () => {
        try {
            const { data } = await api.get('/users/profile');
            set({ user: data });
        } catch (error) {
            console.error(error.message);
        }
    },

    fetchTransactions: async () => {
        try {
            const { data } = await api.get('/accounts/transactions');
            set({ transactions: data });
        } catch (error) {
            console.error(error.message);
        }
    },

    transferFunds: async (recipientAccountNumber, amount) => {
        set({ loading: true, error: null });
        try {
            const { data } = await api.post('/accounts/transfer', { recipientAccountNumber, amount });
            await get().fetchProfile();
            await get().fetchTransactions();
            set({ loading: false });
            return data;
        } catch (error) {
            const message = error.response?.data?.message || error.message;
            set({ error: message, loading: false });
            throw new Error(message);
        }
    },

    fetchAllUsers: async () => {
        try {
            const { data } = await api.get('/users');
            set({ allUsers: data });
        } catch (error) {
            console.error(error.message);
        }
    },

    fetchAllTransactions: async () => {
        try {
            const { data } = await api.get('/accounts/admin/transactions');
            set({ allTransactions: data });
        } catch (error) {
            console.error(error.message);
        }
    },

    fetchInvestments: async () => {
        try {
            const { data } = await api.get('/accounts/investments');
            set({ investments: data });
        } catch (error) {
            console.error(error.message);
        }
    },

    createFD: async (amount, tenureMonths) => {
        set({ loading: true });
        try {
            const { data } = await api.post('/accounts/invest/fd', { amount, tenureMonths });
            await get().fetchProfile();
            await get().fetchInvestments();
            set({ loading: false });
            return data;
        } catch (error) {
            const msg = error.response?.data?.message || error.message;
            set({ error: msg, loading: false });
            throw new Error(msg);
        }
    },

    createRD: async (monthlyDeposit, tenureMonths) => {
        set({ loading: true });
        try {
            const { data } = await api.post('/accounts/invest/rd', { monthlyDeposit, tenureMonths });
            await get().fetchProfile();
            await get().fetchInvestments();
            set({ loading: false });
            return data;
        } catch (error) {
            const msg = error.response?.data?.message || error.message;
            set({ error: msg, loading: false });
            throw new Error(msg);
        }
    },

    clearError: () => set({ error: null })
}));

export default useStore;
