import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getPca } from '../services/api';
import { 
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  LineChart, Line, Legend, AreaChart, Area, Cell 
} from 'recharts';
import { 
  Play, Map, Maximize2, Activity, Info, 
  ChevronRight, Database, TrendingUp, Zap
} from 'lucide-react';

export default function PcaPage() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const handleRun = async () => {
    setLoading(true);
    try {
      const res = await getPca();
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
            <Map className="mr-3 text-emerald-600" size={32} /> Component Analysis
          </h1>
          <p className="text-gray-500 mt-1 pl-11">Reduce feature dimensions into principal orthogonal vectors for multi-variate mapping.</p>
        </div>
        <button 
          onClick={handleRun} 
          disabled={loading}
          className="px-8 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-2xl shadow-lg flex items-center transition-all disabled:opacity-50 text-[10px] font-black uppercase tracking-widest"
        >
          {loading ? <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }} className="mr-2 border-2 border-white border-t-transparent rounded-full w-4 h-4" /> : <Play size={16} className="mr-2" />}
          Decompose Features
        </button>
      </header>

      {error && (
        <div className="p-4 bg-red-50 text-red-600 rounded-3xl border border-red-100 flex items-center shadow-sm">
          <Activity className="mr-3" /> <span className="font-bold">{error}</span>
        </div>
      )}

      <AnimatePresence mode="wait">
        {!data && !error ? (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-[500px] bg-white border border-dashed border-gray-200 rounded-[3rem] flex flex-col items-center justify-center text-center p-12">
            <div className="bg-emerald-50 p-10 rounded-full mb-6 text-emerald-200">
              <Map size={64} />
            </div>
            <h3 className="text-2xl font-black text-gray-800 mb-2">PCA Ready</h3>
            <p className="text-gray-500 max-w-sm">Compute principal components to collapse the dataset's high-dimensional space into interpretable 2D vector maps.</p>
          </motion.div>
        ) : data && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-10">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
               {/* 2D PCA Map */}
               <div className="lg:col-span-2 bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden relative group">
                  <header className="flex justify-between items-center mb-10">
                     <h3 className="text-lg font-black text-gray-800 flex items-center uppercase tracking-tight">
                        <TrendingUp className="mr-2 text-emerald-500" size={20}/> PC1 vs PC2 Projection
                     </h3>
                     <span className="text-[10px] font-black text-emerald-400 bg-emerald-50 px-3 py-1 rounded-full uppercase tracking-tighter">Latent Space Map</span>
                  </header>
                  <div className="h-[400px]">
                    <ResponsiveContainer width="100%" height="100%">
                       <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                          <CartesianGrid strokeDasharray="3 3" vertical={false} strokeOpacity={0.1} />
                          <XAxis type="number" dataKey="pc1" name="PC 1" axisLine={false} tickLine={false} tick={{fontSize: 10, fill: '#9ca3af'}} />
                          <YAxis type="number" dataKey="pc2" name="PC 2" axisLine={false} tickLine={false} tick={{fontSize: 10, fill: '#9ca3af'}} />
                          <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)'}} />
                          <Scatter name="Cars" data={data.scatter} fill="#10b981" fillOpacity={0.6}>
                             {data.scatter.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={index % 2 === 0 ? '#10b981' : '#3b82f6'} />
                             ))}
                          </Scatter>
                       </ScatterChart>
                    </ResponsiveContainer>
                  </div>
               </div>

               {/* Scree Plot */}
               <div className="bg-gray-900 p-8 rounded-[2.5rem] shadow-xl text-white flex flex-col">
                  <header className="flex justify-between items-center mb-8">
                     <h3 className="text-lg font-black flex items-center font-mono tracking-tight text-emerald-400">
                        <Zap className="mr-2" size={18}/> Variance Scree
                     </h3>
                     <Info size={16} className="text-gray-500" />
                  </header>
                  <div className="flex-1 h-[250px]">
                     <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={data.scree}>
                           <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
                           <XAxis dataKey="component" hide />
                           <YAxis axisLine={false} tickLine={false} tick={{fontSize: 10, fill: '#64748b'}} />
                           <Tooltip contentStyle={{backgroundColor: '#0f172a', border: 'none', borderRadius: '12px'}} />
                           <Area type="stepAfter" dataKey="variance" stroke="#10b981" fill="#10b981" fillOpacity={0.1} strokeWidth={3} />
                        </AreaChart>
                     </ResponsiveContainer>
                  </div>
                  <div className="mt-8 bg-white/5 p-6 rounded-3xl border border-white/5 hover:bg-white/10 transition-all cursor-default group">
                     <div className="flex items-center text-[10px] font-black uppercase text-emerald-400 mb-2 tracking-widest">
                        <ChevronRight size={14} className="mr-1 group-hover:translate-x-1 transition-transform" /> Optimization Detail
                     </div>
                     <p className="text-xs text-gray-400 font-medium leading-relaxed">
                        The primary component captures <strong>{(data.explained_variance[0] * 100).toFixed(1)}%</strong> of dataset behavior. Additional components provide residual variance indexing.
                     </p>
                  </div>
               </div>
            </div>

            {/* Weights Display */}
            <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100">
               <h3 className="text-lg font-black text-gray-800 mb-8 flex items-center uppercase tracking-widest">
                  <Database className="mr-2 text-emerald-500" size={16}/> Eigenvalue Matrix
               </h3>
               <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                  {data.eigenvalues.map((val, i) => (
                    <div key={i} className="bg-gray-50 p-6 rounded-3xl border border-gray-100 flex flex-col items-center group hover:bg-emerald-50 hover:border-emerald-100 transition-all">
                       <span className="text-[10px] font-black text-gray-400 mb-1 group-hover:text-emerald-500 uppercase tracking-tighter transition-colors">Vector {i+1}</span>
                       <span className="text-xl font-black text-gray-800">{val.toFixed(3)}</span>
                    </div>
                  ))}
               </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
