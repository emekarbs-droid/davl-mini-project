import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { trainClassification } from '../services/api';
import { 
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  Cell, LineChart, Line, AreaChart, Area, Legend, ZAxis
} from 'recharts';
import { 
  Play, Crosshair, Target, AlertCircle, BarChart as BarIcon, 
  Layers, Database, PieChart as PieIcon, Activity
} from 'lucide-react';

const COLORS = {
  'Low': '#10b981',    // Emerald
  'Medium': '#3b82f6', // Blue
  'High': '#ef4444'    // Red
};

export default function ClassificationPage() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const handleTrain = async () => {
    setLoading(true);
    try {
      const res = await trainClassification({
        target_column: 'price',
        features: [] 
      });
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
            <Crosshair className="mr-3 text-red-600" size={32} /> Classification Engine
          </h1>
          <p className="text-gray-500 mt-1 pl-11">Categorize vehicles into Low, Medium, or High value segments via Logistic Probability.</p>
        </div>
        <button 
          onClick={handleTrain} 
          disabled={loading}
          className="px-8 py-3 bg-red-600 hover:bg-red-700 text-white rounded-2xl shadow-lg flex items-center transition-all disabled:opacity-50 text-[10px] font-black uppercase tracking-widest"
        >
          {loading ? <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }} className="mr-2 border-2 border-white border-t-transparent rounded-full w-4 h-4" /> : <Play size={16} className="mr-2" />}
          Train Logistic Model
        </button>
      </header>

      {error && (
        <div className="p-4 bg-red-50 text-red-600 rounded-3xl border border-red-100 flex items-center shadow-sm">
          <AlertCircle className="mr-3" /> <span className="font-bold">{error}</span>
        </div>
      )}

      <AnimatePresence mode="wait">
        {!data && !error ? (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-[500px] bg-white border border-dashed border-gray-200 rounded-[3rem] flex flex-col items-center justify-center text-center p-12">
            <div className="bg-red-50 p-10 rounded-full mb-6 text-red-200">
              <Layers size={64} />
            </div>
            <h3 className="text-2xl font-black text-gray-800 mb-2">Classifier Ready</h3>
            <p className="text-gray-500 max-w-sm">Initialize the Logistic Regression pipeline to generate categorical bounds and probability curves.</p>
          </motion.div>
        ) : data && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-10">
            {/* Accuracy & Metrics Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
               <div className="lg:col-span-1 bg-white p-10 rounded-[2.5rem] shadow-sm border border-gray-100 flex flex-col items-center justify-center text-center relative overflow-hidden">
                  <div className="absolute top-0 right-0 p-4 opacity-5 rotate-12">
                     <PieIcon size={120} />
                  </div>
                  <Target size={48} className="text-red-500 mb-6" />
                  <h3 className="text-6xl font-black text-gray-900 leading-none">{(data.accuracy * 100).toFixed(1)}<span className="text-2xl font-black text-red-400 -ml-1">%</span></h3>
                  <p className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 mt-4 mb-2">Model Accuracy Score</p>
                  <div className="w-16 h-1 bg-red-100 rounded-full"></div>
               </div>

               {/* Confusion Matrix */}
               <div className="lg:col-span-2 bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100">
                  <h3 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-8 flex items-center">
                     <BarIcon size={16} className="mr-2 text-red-500" /> Confusion Matrix (Actual vs Pred)
                  </h3>
                  <div className="grid grid-cols-4 gap-2">
                     <div className="col-span-1"></div>
                     {data.labels.map(l => <div key={l} className="text-center text-[10px] font-black text-gray-400 uppercase pb-2">{l}</div>)}
                     
                     {data.confusion_matrix.map((row, i) => (
                        <>
                           <div key={`label-${i}`} className="flex items-center justify-end pr-4 text-[10px] font-black text-gray-400 uppercase">{data.labels[i]}</div>
                           {row.map((val, j) => {
                              const total = row.reduce((a,b) => a+b, 0);
                              const opacity = val / (total || 1);
                              return (
                                 <div 
                                    key={`val-${i}-${j}`} 
                                    className={`aspect-square rounded-2xl flex items-center justify-center text-xl font-black transition-all hover:scale-105 ${i === j ? 'bg-red-500 text-white shadow-lg' : 'bg-gray-50 text-gray-300'}`}
                                    style={{ opacity: i === j ? 0.3 + (opacity * 0.7) : 1 }}
                                 >
                                    {val}
                                 </div>
                              );
                           })}
                        </>
                     ))}
                  </div>
               </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
               {/* Decision Boundary */}
               <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden relative group">
                  <header className="flex justify-between items-center mb-8">
                     <h3 className="text-lg font-black text-gray-800 flex items-center uppercase tracking-tight">
                        <Activity className="mr-2 text-red-500" size={18}/> Decision Boundaries
                     </h3>
                     <div className="flex space-x-2">
                        {Object.entries(COLORS).map(([label, color]) => (
                           <span key={label} className="text-[8px] font-black uppercase text-gray-400 flex items-center">
                              <div className="w-2 h-2 rounded-full mr-1" style={{ backgroundColor: color }}></div> {label}
                           </span>
                        ))}
                     </div>
                  </header>
                  <div className="h-[400px]">
                    <ResponsiveContainer width="100%" height="100%">
                       <ScatterChart margin={{ top: 10, right: 10, bottom: 0, left: 10 }}>
                          <XAxis type="number" dataKey="x" hide />
                          <YAxis type="number" dataKey="y" hide />
                          <ZAxis type="number" range={[100, 100]} />
                          <Scatter name="Boundary" data={data.decision_mesh}>
                             {data.decision_mesh.map((entry, index) => (
                                <Cell key={`mesh-${index}`} fill={COLORS[entry.label]} fillOpacity={0.05} />
                             ))}
                          </Scatter>
                          <Scatter name="Observations" data={data.scatter} shape="circle">
                             {data.scatter.map((entry, index) => (
                                <Cell key={`point-${index}`} fill={COLORS[entry.label]} strokeWidth={2} stroke="white" />
                             ))}
                          </Scatter>
                          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                       </ScatterChart>
                    </ResponsiveContainer>
                  </div>
               </div>

               {/* Probability Sigmoid */}
               <div className="bg-gray-900 p-8 rounded-[2.5rem] shadow-xl text-white overflow-hidden">
                  <header className="flex justify-between items-center mb-8">
                     <h3 className="text-lg font-black flex items-center font-mono tracking-tight text-red-400">
                        <Activity size={18} className="mr-2"/> Sigmoid Curve (High Class)
                     </h3>
                  </header>
                  <div className="h-[400px]">
                    <ResponsiveContainer width="100%" height="100%">
                       <AreaChart data={data.sigmoid}>
                          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
                          <XAxis dataKey="x" hide />
                          <YAxis domain={[0, 1]} tick={{fill: '#64748b', fontSize: 10}} axisLine={false} tickLine={false} />
                          <Tooltip contentStyle={{backgroundColor: '#0f172a', border: 'none', borderRadius: '12px'}} />
                          <Area type="monotone" dataKey="prob" stroke="#ef4444" strokeWidth={3} fill="url(#colorSig)" animateDuration={2000} />
                          <defs>
                             <linearGradient id="colorSig" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                                <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                             </linearGradient>
                          </defs>
                       </AreaChart>
                    </ResponsiveContainer>
                  </div>
                  <p className="text-[10px] text-gray-500 mt-4 uppercase text-center font-black tracking-widest italic opacity-60">Logistic S-Curve: Probability of being 'High' category vehicle</p>
               </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
