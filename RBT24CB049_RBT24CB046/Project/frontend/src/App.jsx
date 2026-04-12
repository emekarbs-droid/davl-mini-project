import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';
import useStore from './store/useStore';

function App() {
  const { user } = useStore();

  const getRedirectPath = () => {
    if (!user) return '/';
    return user.isAdmin ? '/admin' : '/dashboard';
  };

  return (
    <Router>
      <div className="bg-[#0f172a] min-h-screen text-slate-100 selection:bg-blue-500/30 selection:text-blue-200">
        <Routes>
          <Route 
            path="/" 
            element={user ? <Navigate to={getRedirectPath()} replace /> : <LandingPage />} 
          />
          <Route 
            path="/dashboard" 
            element={user ? (user.isAdmin ? <Navigate to="/admin" replace /> : <Dashboard />) : <Navigate to="/" replace />} 
          />
          <Route 
            path="/admin" 
            element={user?.isAdmin ? <AdminDashboard /> : <Navigate to="/" replace />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
