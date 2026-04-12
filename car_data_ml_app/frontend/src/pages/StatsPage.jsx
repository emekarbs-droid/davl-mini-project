import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getEdaSummary, getScatterData } from '../services/api';
import { 
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  BarChart, Bar, ZAxis, Cell
} from 'recharts';
import { 
  BarChart2, Activity, AlertCircle, Hash, Grid, Maximize2, 
  ChevronDown, ChevronUp, Shuffle, Info, Database 
} from 'lucide-react';

export default function StatsPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [scatterX, setScatterX] = useState('horsepower');
  const [scatterY, setScatterY] = useState('price');
  const [scatterData, setScatterData] = useState([]);

  useEffect(() => {
    fetchMainData();
  }, []);

  useEffect(() => {
    if (data) fetchScatter();
  }, [scatterX, scatterY, data]);

  const fetchMainData = async () => {
    try {
      const res = await getEdaSummary();
      setData(res);
      setScatterX(res.columns.numeric[0] || 'horsepower');
      setScatterY(res.columns.numeric[1] || res.columns.numeric[0] || 'price');
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
    setLoading(false);
  };

  const fetchScatter = async () => {
    if (!scatterX || !scatterY) return;
    try {
      const res = await getScatterData(scatterX, scatterY);
      setScatterData(Array.isArray(res) ? res : []);
    } catch (err) {
      console.error("Scatter fetch fail", err);
    }
  };

  if (loading) return (
    <div className="flex h-full items-center justify-center p-20">
      <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }} className="text-emerald-600">
        <Activity size={48} />
      </motion.div>
    </div>
  );

  if (error || !data) return (
    <div className="p-12 text-center">
      <AlertCircle size={64} className="mx-auto text-red-400 mb-4" />
      <h2 className="text-2xl font-bold text-gray-800">Statistics Locked</h2>
      <p className="text-gray-500 mt-2">{error || "Upload a dataset first to unlock the deep statistical analytical suite."}</p>
    </div>
  );

  const numericCols = data.columns?.numeric || [];
  const correlationMatrix = data.correlation || {};

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-8 pb-24 max-w-7xl mx-auto space-y-10">
      <header>
        <h1 className="text-3xl font-black text-gray-900 flex items-center">
          <BarChart2 className="mr-3 text-emerald-600" size={32} /> Statistics Analysis
        </h1>
        <p className="text-gray-500 mt-1 pl-11">Advanced descriptive metrics, covariance, and pairwise correlation mappings.</p>
      </header>

      {/* Descriptive Stats Table */}
      <section className="bg-white rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden">
        <div className="p-6 border-b border-gray-50 bg-gray-50/50 flex items-center justify-between">
            <h3 className="text-lg font-extrabold text-gray-800 flex items-center">
                <Grid className="mr-2 text-emerald-500" size={18} /> Descriptive Matrix
            </h3>
            <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">Numerical Properties</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-500">
            <thead className="text-[10px] text-gray-400 uppercase bg-gray-50/30">
              <tr>
                <th className="py-4 px-6 border-b border-gray-100">Feature</th>
                <th className="py-4 px-6 border-b border-gray-100">Mean</th>
                <th className="py-4 px-6 border-b border-gray-100">Median</th>
                <th className="py-4 px-6 border-b border-gray-100">SD (σ)</th>
                <th className="py-4 px-6 border-b border-gray-100">Min</th>
                <th className="py-4 px-6 border-b border-gray-100">Max</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {numericCols.map(col => (
                <tr key={col} className="hover:bg-emerald-50/20 transition-colors">
                  <td className="py-4 px-6 font-bold text-gray-900 capitalize">{col.replace(/_/g, ' ')}</td>
                  <td className="py-4 px-6">{(data.stats?.[col]?.mean || 0).toLocaleString(undefined, {maximumFractionDigits:2})}</td>
                  <td className="py-4 px-6">{(data.stats?.[col]?.median || 0).toLocaleString(undefined, {maximumFractionDigits:2})}</td>
                  <td className="py-4 px-6 bg-gray-50/20 text-gray-400">{(data.stats?.[col]?.std || 0).toLocaleString(undefined, {maximumFractionDigits:2})}</td>
                  <td className="py-4 px-6 font-medium text-red-400">{data.stats?.[col]?.min ?? 0}</td>
                  <td className="py-4 px-6 font-medium text-emerald-500">{data.stats?.[col]?.max ?? 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        {/* Heatmap Section */}
        <section className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 relative group">
           <h3 className="text-xl font-extrabold text-gray-800 mb-8 flex items-center">
             <Hash className="mr-2 text-emerald-500" size={20} /> Correlation Heatmap
           </h3>
           <div className="flex flex-col space-y-2">
             <div className="flex">
               <div className="w-24"></div>
               <div className="flex flex-1">
                 {numericCols.map(col => (
                   <div key={col} className="flex-1 text-[8px] font-black uppercase tracking-tighter text-center rotate-45 h-12 flex items-end justify-center pb-2 text-gray-400 truncate">
                     {col}
                   </div>
                 ))}
               </div>
             </div>
             {numericCols.map(row => (
               <div key={row} className="flex h-12">
                 <div className="w-24 flex items-center pr-3 justify-end text-[10px] font-bold text-gray-500 uppercase truncate">
                   {row}
                 </div>
                 <div className="flex flex-1 gap-1">
                    {numericCols.map(col => {
                      const val = correlationMatrix[row]?.[col] ?? 0;
                      const color = val > 0 ? `rgba(16, 185, 129, ${val})` : `rgba(239, 68, 68, ${Math.abs(val)})`;
                      return (
                        <motion.div 
                          initial={{ scale: 0 }} animate={{ scale: 1 }}
                          key={col} 
                          className="flex-1 rounded-sm flex items-center justify-center text-[10px] font-bold text-white relative group/tile"
                          style={{ backgroundColor: color }}
                          title={`${row} vs ${col}: ${val.toFixed(2)}`}
                        >
                           <span className="opacity-0 group-hover/tile:opacity-100 transition-opacity">{(val * 100).toFixed(0)}</span>
                        </motion.div>
                      );
                    })}
                 </div>
               </div>
             ))}
           </div>
           <div className="mt-8 flex justify-center items-center space-x-6">
              <div className="flex items-center text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                 <div className="w-4 h-4 bg-red-400 rounded-sm mr-2"></div> Negative (-1.0)
              </div>
              <div className="flex items-center text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                 <div className="w-4 h-4 bg-gray-100 rounded-sm mr-2 border border-gray-200"></div> Neutral (0.0)
              </div>
              <div className="flex items-center text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                 <div className="w-4 h-4 bg-emerald-500 rounded-sm mr-2 shadow-sm"></div> Positive (+1.0)
              </div>
           </div>
        </section>

        {/* Dynamic Scatter Plot */}
        <section className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 flex flex-col">
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-xl font-extrabold text-gray-800 flex items-center">
              <Activity className="mr-2 text-emerald-500" size={20} /> Pairwise Scatter
            </h3>
            <div className="flex bg-gray-50 p-1.5 rounded-2xl border border-gray-100 space-x-2">
                <select 
                  value={scatterX} 
                  onChange={(e) => setScatterX(e.target.value)}
                  className="bg-white px-3 py-1 text-[10px] font-black uppercase tracking-widest text-emerald-600 rounded-xl outline-none shadow-sm cursor-pointer border-none appearance-none"
                >
                  {numericCols.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
                <Shuffle size={14} className="text-gray-300 self-center" />
                <select 
                  value={scatterY} 
                  onChange={(e) => setScatterY(e.target.value)}
                  className="bg-white px-3 py-1 text-[10px] font-black uppercase tracking-widest text-blue-600 rounded-xl outline-none shadow-sm cursor-pointer border-none appearance-none"
                >
                   {numericCols.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
            </div>
          </div>
          
          <div className="flex-1 h-[350px]">
            <ResponsiveContainer width="100%" height="100%">
               <ScatterChart margin={{ top: 10, right: 10, bottom: 0, left: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} strokeOpacity={0.1} />
                  <XAxis type="number" dataKey={scatterX} name={scatterX} axisLine={false} tickLine={false} tick={{fontSize: 10}} label={{ value: scatterX, position: 'insideBottom', offset: -5, fontSize: 10, fill: '#9ca3af', fontWeight: 'bold' }} />
                  <YAxis type="number" dataKey={scatterY} name={scatterY} axisLine={false} tickLine={false} tick={{fontSize: 10}} label={{ value: scatterY, angle: -90, position: 'insideLeft', fontSize: 10, fill: '#9ca3af', fontWeight: 'bold' }} />
                  <ZAxis type="number" range={[40, 40]} />
                  <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)' }} />
                  <Scatter name="Observations" data={scatterData} fill="#10b981" fillOpacity={0.6}>
                    {scatterData.map((entry, index) => (
                       <Cell key={`cell-${index}`} fill={index % 2 === 0 ? '#10b981' : '#3b82f6'} />
                    ))}
                  </Scatter>
               </ScatterChart>
            </ResponsiveContainer>
          </div>
        </section>
      </div>

      {/* Boxplots Display */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {numericCols.slice(0, 6).map((col, idx) => (
          <div key={col} className="bg-white p-6 rounded-[2rem] shadow-sm border border-gray-100 flex flex-col items-center">
             <h4 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-6 flex items-center">
                <Maximize2 size={14} className="mr-2"/> {col.replace(/_/g, ' ')} Boxplot
             </h4>
             <div className="w-full flex justify-between px-4 mb-2">
                 <span className="text-[10px] font-bold text-red-300">Min: {data.boxplots?.[col]?.min ?? 0}</span>
                 <span className="text-[10px] font-bold text-emerald-400">Max: {data.boxplots?.[col]?.max ?? 0}</span>
             </div>
             <div className="w-full relative h-16 bg-gray-50 rounded-2xl flex items-center group overflow-hidden">
                {/* Outlier range line */}
                <div className="absolute h-0.5 bg-gray-200 left-[10%] right-[10%] group-hover:bg-emerald-100 transition-colors"></div>
                {/* Inter-quartile range box */}
                <div 
                   className="absolute h-8 bg-emerald-500 rounded-sm border-2 border-emerald-600 shadow-md group-hover:scale-y-110 transition-transform" 
                   style={{ left: '30%', width: '40%' }}
                >
                   {/* Median line */}
                   <div className="absolute top-0 bottom-0 left-1/2 w-0.5 bg-emerald-200"></div>
                </div>
             </div>
             <div className="mt-4 text-[10px] font-bold text-gray-400 flex space-x-4">
                <span className="flex items-center"><div className="w-2 h-2 rounded-full bg-emerald-500 mr-1"></div> {(data.boxplots?.[col]?.median ?? 0).toFixed(1)} Median</span>
                <span className="text-gray-300">IQR Spread: {((data.boxplots?.[col]?.q3 ?? 0) - (data.boxplots?.[col]?.q1 ?? 0)).toFixed(1)}</span>
             </div>
          </div>
        ))}
      </section>
    </motion.div>
  );
}
