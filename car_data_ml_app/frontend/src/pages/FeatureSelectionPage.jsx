import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getFeatureRank } from '../services/api';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell 
} from 'recharts';
import { 
  ListChecks, Target, AlertCircle, Award, Database, 
  Activity, ArrowUpCircle, Info, Filter 
} from 'lucide-react';

export default function FeatureSelectionPage() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRanking();
  }, []);

  const fetchRanking = async () => {
    setLoading(true);
    try {
      const res = await getFeatureRank();
      setData(res);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
    setLoading(false);
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-8 pb-32 max-w-7xl mx-auto space-y-10">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-black text-gray-900 flex items-center">
            <ListChecks className="mr-3 text-blue-600" size={32} /> Feature Selection
          </h1>
          <p className="text-gray-500 mt-1 pl-11">Evaluate feature significance using RFE and Chi-Square variance statistical ranking.</p>
        </div>
        <button 
          onClick={fetchRanking} 
          disabled={loading}
          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl shadow-lg flex items-center transition-all disabled:opacity-50 text-[10px] font-black uppercase tracking-widest"
        >
          {loading ? <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }} className="mr-2 border-2 border-white border-t-transparent rounded-full w-3 h-3" /> : <Filter size={14} className="mr-2" />}
          Refresh Rankings
        </button>
      </header>

      {error && (
        <div className="p-4 bg-red-50 text-red-600 rounded-3xl border border-red-100 flex items-center">
          <AlertCircle className="mr-3" /> <span className="font-bold">{error}</span>
        </div>
      )}

      <AnimatePresence mode="wait">
        {!data && !error ? (
          <div className="h-[500px] flex items-center justify-center">
             <motion.div animate={{ scale: [1, 1.1, 1] }} transition={{ repeat: Infinity, duration: 2 }} className="text-blue-200">
                <Database size={80} />
             </motion.div>
          </div>
        ) : data && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-10">
             
             <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
                {/* Ranking Bar Chart */}
                <div className="lg:col-span-2 bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 flex flex-col">
                   <header className="flex justify-between items-center mb-10">
                      <h3 className="text-xl font-black text-gray-800 flex items-center uppercase tracking-tight">
                         <Activity className="mr-2 text-blue-500" size={20}/> Predictive Importance Score
                      </h3>
                      <span className="text-[10px] font-black text-blue-400 bg-blue-50 px-3 py-1 rounded-full uppercase italic">Statistical Significance</span>
                   </header>
                   <div className="flex-1 h-[400px]">
                      <ResponsiveContainer width="100%" height="100%">
                         <BarChart data={data.rankings} layout="vertical" margin={{ left: 20 }}>
                            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f3f4f6" />
                            <XAxis type="number" axisLine={false} tickLine={false} tick={{fontSize: 10, fill: '#9ca3af'}} />
                            <YAxis type="category" dataKey="feature" axisLine={false} tickLine={false} tick={{fontSize: 10, fontWeight: 'bold', fill: '#4b5563'}} />
                            <Tooltip cursor={{fill: '#f9fafb'}} contentStyle={{borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)'}} />
                            <Bar dataKey="score" fill="#3b82f6" radius={[0, 10, 10, 0]} barSize={25}>
                               {data.rankings.map((entry, index) => (
                                  <Cell key={`cell-${index}`} fill={index < 5 ? '#3b82f6' : '#e5e7eb'} />
                               ))}
                            </Bar>
                         </BarChart>
                      </ResponsiveContainer>
                   </div>
                </div>

                {/* Recommended Features Card */}
                <div className="bg-gradient-to-br from-gray-900 to-black p-8 rounded-[2.5rem] shadow-2xl text-white flex flex-col overflow-hidden relative">
                   <div className="relative z-10">
                      <h3 className="text-xl font-black mb-6 flex items-center text-blue-400">
                        <Award className="mr-2" /> Top Selections
                      </h3>
                      <p className="text-xs text-gray-400 mb-8 font-medium leading-relaxed">
                        Based on Recursive Feature Elimination (RFE), these features demonstrate the highest weight variance for car price estimation.
                      </p>
                      
                      <div className="space-y-4">
                         {data.selected_rfe.map((feat, i) => (
                            <motion.div 
                              key={feat} 
                              initial={{ x: 20, opacity: 0 }} 
                              animate={{ x: 0, opacity: 1 }}
                              transition={{ delay: i * 0.1 }}
                              className="bg-white/10 p-4 rounded-2xl flex items-center justify-between group hover:bg-white/20 transition-all border border-white/5"
                            >
                               <div className="flex items-center">
                                  <span className="text-[10px] font-black text-blue-400 mr-3 opacity-50">0{i+1}</span>
                                  <span className="text-sm font-bold capitalize">{feat.replace(/_/g, ' ')}</span>
                               </div>
                               <ArrowUpCircle size={16} className="text-emerald-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                            </motion.div>
                         ))}
                      </div>

                      <div className="mt-10 bg-blue-500/10 p-5 rounded-3xl border border-blue-500/20">
                         <div className="flex items-center text-blue-300 text-[10px] font-black uppercase tracking-[0.2em] mb-2">
                           <Info size={14} className="mr-2"/> Algorithm Note
                         </div>
                         <p className="text-[10px] text-gray-500 leading-normal italic">
                           Variance thresholds are used to prune features with extremely low constant distributions before RFE ranking.
                         </p>
                      </div>
                   </div>
                   <div className="absolute -bottom-10 -right-10 opacity-10">
                      <ListChecks size={200} />
                   </div>
                </div>
             </div>

             {/* Detailed Ranking Table */}
             <div className="bg-white rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden">
                <div className="p-6 border-b border-gray-50 flex items-center border-dashed">
                  <h3 className="text-lg font-black text-gray-800 flex items-center">
                     Detailed Scoring Matrix
                  </h3>
                </div>
                <div className="overflow-x-auto">
                   <table className="w-full text-left text-sm text-gray-500">
                      <thead className="bg-gray-50/50 text-[10px] font-black uppercase tracking-widest text-gray-400">
                         <tr>
                            <th className="py-4 px-8 border-b border-gray-100">Feature Name</th>
                            <th className="py-4 px-8 border-b border-gray-100">Variance Score</th>
                            <th className="py-4 px-8 border-b border-gray-100">F-Statistic</th>
                            <th className="py-4 px-8 border-b border-gray-100">RFE Rank</th>
                         </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-50 font-medium">
                         {data.rankings.map((row, i) => (
                            <tr key={i} className={`hover:bg-blue-50/30 transition-colors ${i < 5 ? 'bg-blue-50/10' : ''}`}>
                               <td className="py-5 px-8 flex items-center">
                                  {i < 5 && <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mr-3 shadow-sm shadow-blue-200"></div>}
                                  <span className={i < 5 ? 'font-black text-gray-900' : 'text-gray-500 capitalize'}>{row.feature}</span>
                               </td>
                               <td className="py-5 px-8 font-mono text-xs">{row.variance.toExponential(2)}</td>
                               <td className="py-5 px-8">{row.f_score.toFixed(2)}</td>
                               <td className={`py-5 px-8 text-xs font-black italic ${row.rfe_rank === 1 ? 'text-emerald-600' : ''}`}>
                                 No. {row.rfe_rank}
                               </td>
                            </tr>
                         ))}
                      </tbody>
                   </table>
                </div>
             </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
