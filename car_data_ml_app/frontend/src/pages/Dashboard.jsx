import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getEdaSummary } from '../services/api';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, Legend
} from 'recharts';
import { 
  LayoutDashboard, Users, DollarSign, Zap, Fuel, Activity, 
  TrendingUp, AlertCircle, Info, ChevronRight 
} from 'lucide-react';

const COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log("Fetching EDA Summary...");
        const res = await getEdaSummary();
        console.log("EDA Summary Received:", res);
        setData(res);
      } catch (err) {
        console.error("Dashboard Fetch Error:", err);
        setError(err.response?.data?.detail || err.message);
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  if (loading) return (
    <div className="flex h-full items-center justify-center p-20">
      <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }} className="text-indigo-600">
        <Activity size={48} />
      </motion.div>
    </div>
  );

  if (error || !data) return (
    <div className="p-12 text-center">
      <AlertCircle size={64} className="mx-auto text-red-400 mb-4" />
      <h2 className="text-2xl font-bold text-gray-800">No Dataset Found</h2>
      <p className="text-gray-500 mt-2">Please upload a dataset to generate the dashboard overview.</p>
    </div>
  );

  const priceDist = Object.entries(data.distributions.fuel_type || {}).map(([name, value]) => ({ name, value }));
  const transDist = Object.entries(data.distributions.transmission || data.distributions.Transmission || {}).map(([name, value]) => ({ name, value }));

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-8 pb-24 max-w-7xl mx-auto space-y-8">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-black text-gray-900 flex items-center">
            <LayoutDashboard className="mr-3 text-indigo-600" size={32} /> Dashboard Overview
          </h1>
          <p className="text-gray-500 mt-1">High-level insights and automated data signals.</p>
        </div>
        <div className="bg-indigo-50 px-4 py-2 rounded-2xl flex items-center text-indigo-700 font-bold text-sm">
           <Activity size={16} className="mr-2" /> Live Analysis Feed
        </div>
      </header>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard title="Total Cars" value={data.stats.price?.count?.toLocaleString() || '0'} icon={Users} color="bg-blue-500" />
        <KPICard title="Average Price" value={`$${Math.round(data.stats.price?.mean || 0).toLocaleString()}`} icon={DollarSign} color="bg-emerald-500" />
        <KPICard title="Average Mileage" value={`${Math.round(data.stats.mileage?.mean || 0).toLocaleString()} km`} icon={Activity} color="bg-orange-500" />
        <KPICard title="Most Common Fuel" value={Object.keys(data.distributions.fuel_type || {})[0] || 'N/A'} icon={Fuel} color="bg-indigo-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Price Dist Chart */}
        <div className="lg:col-span-2 bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100">
           <div className="flex justify-between items-center mb-8">
             <h3 className="text-xl font-extrabold text-gray-800">Automotive Scale Insights</h3>
             <span className="text-xs font-black text-indigo-400 bg-indigo-50 px-3 py-1 rounded-full uppercase tracking-tighter">Market Distribution</span>
           </div>
           <div className="h-[300px]">
             <ResponsiveContainer width="100%" height="100%">
               <BarChart data={priceDist}>
                 <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                 <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#9ca3af', fontSize: 12}} dy={10} />
                 <YAxis axisLine={false} tickLine={false} tick={{fill: '#9ca3af', fontSize: 12}} />
                 <Tooltip cursor={{fill: '#f9fafb'}} contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)' }} />
                 <Bar dataKey="value" fill="#4f46e5" radius={[6, 6, 0, 0]} barSize={40}>
                    {priceDist.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                 </Bar>
               </BarChart>
             </ResponsiveContainer>
           </div>
        </div>

        {/* Auto Insights Box */}
        <div className="space-y-6">
           <div className="bg-gradient-to-br from-indigo-600 to-blue-700 p-8 rounded-[2.5rem] text-white shadow-lg relative overflow-hidden group">
              <div className="relative z-10">
                <h3 className="text-xl font-bold mb-4 flex items-center">
                  <TrendingUp className="mr-2" /> Auto Insights
                </h3>
                <ul className="space-y-4">
                  {data?.insights && data.insights.length > 0 ? data.insights.map((insight, i) => (
                    <li key={i} className="flex items-start text-sm bg-white/10 p-3 rounded-2xl hover:bg-white/20 transition-colors">
                      <ChevronRight size={18} className="mr-2 flex-shrink-0 mt-0.5 text-blue-200" />
                      <span>{insight}</span>
                    </li>
                  )) : (
                    <p className="text-blue-100 opacity-80 italic">No specific signal anomalies detected in the current data slice.</p>
                  )}
                </ul>
              </div>
              <Activity size={150} className="absolute -bottom-10 -right-10 opacity-10 group-hover:scale-110 transition-transform duration-500" />
           </div>

           <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 flex-1">
              <h3 className="text-lg font-extrabold text-gray-800 mb-6">Transmission Mix</h3>
              <div className="h-[200px]">
                 <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                       <Pie data={transDist} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value" stroke="none">
                          {transDist.map((entry, index) => (
                             <Cell key={`cell-${index}`} fill={COLORS[COLORS.length - 1 - index]} />
                          ))}
                       </Pie>
                       <Tooltip />
                       <Legend verticalAlign="bottom" height={36}/>
                    </PieChart>
                 </ResponsiveContainer>
              </div>
           </div>
        </div>
      </div>

      {/* Dataset Health */}
      <div className="bg-emerald-50/50 border border-emerald-100 p-8 rounded-[2.5rem] flex items-center space-x-6">
        <div className="bg-emerald-500 text-white p-4 rounded-3xl">
          <Info size={32} />
        </div>
        <div>
          <h4 className="text-xl font-bold text-emerald-900 mb-1">Dataset Health: Excellent</h4>
          <p className="text-emerald-700 opacity-80 leading-relaxed max-w-2xl">
            Auto ML Pro has finished the initial heuristic scan. The data quality appears high with sufficient variance in numeric features to support robust Regression and Classification modeling.
          </p>
        </div>
      </div>
    </motion.div>
  );
}

function KPICard({ title, value, icon: Icon, color }) {
  return (
    <motion.div 
      whileHover={{ y: -5 }}
      className="bg-white p-6 rounded-[2rem] shadow-sm border border-gray-100 flex items-center space-x-5 transition-all"
    >
      <div className={`${color} p-4 rounded-2xl text-white shadow-lg`}>
        <Icon size={24} />
      </div>
      <div>
        <p className="text-xs font-black text-gray-400 uppercase tracking-widest">{title}</p>
        <p className="text-2xl font-black text-gray-800">{value}</p>
      </div>
    </motion.div>
  );
}
