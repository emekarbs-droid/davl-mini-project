import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { trainKmeans, getHierarchical } from '../services/api';
import { 
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  Cell, LineChart, Line, ZAxis
} from 'recharts';
import { 
  Network, Play, Grid, Activity, TrendingUp, Info, 
  Layers, Package, ChevronRight, Zap, AlertCircle 
} from 'lucide-react';

const COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function ClusteringPage() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [dendro, setDendro] = useState(null);
  const [error, setError] = useState(null);
  const [clusters, setClusters] = useState(3);

  const handleRun = async () => {
    setLoading(true);
    try {
      const res = await trainKmeans({ n_clusters: clusters });
      const d = await getHierarchical();
      setData(res);
      setDendro(d);
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
            <Network className="mr-3 text-indigo-600" size={32} /> Market Segmentation
          </h1>
          <p className="text-gray-500 mt-1 pl-11">Unsupervised learning discovery to categorize cars into unique market clusters.</p>
        </div>
        <div className="flex bg-white p-2 rounded-3xl shadow-sm border border-gray-50 items-center space-x-4">
           <div className="flex items-center px-4 py-2 bg-gray-50 rounded-2xl">
              <span className="text-[10px] font-black uppercase text-gray-400 mr-3">Clusters (K)</span>
              <input 
                type="number" 
                value={clusters} 
                onChange={(e) => setClusters(Number(e.target.value))} 
                min="2" max="6"
                className="w-10 bg-transparent text-sm font-black text-indigo-600 outline-none"
              />
           </div>
           <button 
              onClick={handleRun} 
              disabled={loading}
              className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl shadow-lg flex items-center transition-all disabled:opacity-50 text-[10px] font-black uppercase tracking-widest"
            >
              {loading ? <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }} className="mr-2 border-2 border-white border-t-transparent rounded-full w-3 h-3" /> : <Play size={14} className="mr-2" />}
              Run Algorithm
            </button>
        </div>
      </header>

      {error && (
        <div className="p-4 bg-red-50 text-red-600 rounded-3xl border border-red-100 flex items-center shadow-sm">
          <AlertCircle className="mr-3" /> <span className="font-bold">{error}</span>
        </div>
      )}

      <AnimatePresence mode="wait">
        {!data && !error ? (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-[500px] bg-white border border-dashed border-gray-200 rounded-[3rem] flex flex-col items-center justify-center text-center p-12">
            <div className="bg-indigo-50 p-10 rounded-full mb-6 text-indigo-200">
              <Network size={64} />
            </div>
            <h3 className="text-2xl font-black text-gray-800 mb-2">Segmentation Ready</h3>
            <p className="text-gray-500 max-w-sm">Execute the clustering pipeline to group vehicles into Budget, Premium, and Signature clusters automatically.</p>
          </motion.div>
        ) : data && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-10">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
               {/* 2D Segment Plot */}
               <div className="lg:col-span-2 bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 relative">
                  <header className="flex justify-between items-center mb-8">
                     <h3 className="text-lg font-black text-gray-800 flex items-center uppercase tracking-tight">
                        <Grid className="mr-2 text-indigo-500" size={18}/> Cluster Distribution (2D)
                     </h3>
                     <div className="flex space-x-3">
                        {Array.from({length: clusters}).map((_, i) => (
                           <div key={i} className="flex items-center text-[8px] font-black text-gray-400 uppercase">
                              <div className="w-2 h-2 rounded-full mr-1" style={{backgroundColor: COLORS[i % COLORS.length]}}></div> C{i+1}
                           </div>
                        ))}
                     </div>
                  </header>
                  <div className="h-[400px]">
                    <ResponsiveContainer width="100%" height="100%">
                       <ScatterChart margin={{ top: 10, right: 10, bottom: 0, left: 10 }}>
                          <XAxis type="number" dataKey="x" hide />
                          <YAxis type="number" dataKey="y" hide />
                          <ZAxis type="number" range={[100, 100]} />
                          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                          <Scatter name="Cars" data={data.scatter}>
                             {data.scatter.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[entry.cluster % COLORS.length]} strokeWidth={2} stroke="white" />
                             ))}
                          </Scatter>
                       </ScatterChart>
                    </ResponsiveContainer>
                  </div>
               </div>

               {/* Elbow Curve */}
               <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 flex flex-col">
                  <header className="flex justify-between items-center mb-10">
                     <h3 className="text-lg font-black text-gray-800 flex items-center uppercase tracking-tight">
                        <Zap className="mr-2 text-indigo-500" size={18}/> Optimal K (Elbow)
                     </h3>
                  </header>
                  <div className="flex-1 h-[250px]">
                     <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={data.elbow}>
                           <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                           <XAxis dataKey="k" axisLine={false} tickLine={false} tick={{fontSize: 10, fill: '#9ca3af'}} />
                           <YAxis axisLine={false} tickLine={false} tick={{fontSize: 10, fill: '#9ca3af'}} />
                           <Tooltip />
                           <Line type="monotone" dataKey="inertia" stroke="#4f46e5" strokeWidth={3} dot={{r: 6, fill: '#4f46e5'}} activeDot={{r: 8}} />
                        </LineChart>
                     </ResponsiveContainer>
                  </div>
                  <div className="mt-8 bg-indigo-50 p-6 rounded-3xl">
                     <div className="flex items-center text-indigo-600 text-[10px] font-black uppercase mb-1">
                        <Info size={14} className="mr-2"/> Interpretation
                     </div>
                     <p className="text-xs text-gray-500 font-medium italic leading-relaxed">
                        The "elbow" point indicates where adding more clusters provides diminishing returns in data variance explanation.
                     </p>
                  </div>
               </div>
            </div>

            {/* Dendrogram Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
               {/* SVG Dendrogram */}
               <div className="bg-gray-900 p-8 rounded-[2.5rem] shadow-xl text-white">
                  <h3 className="text-lg font-black mb-8 flex items-center font-mono text-indigo-400">
                     <Layers className="mr-2" size={18}/> Hierarchical Dendrogram
                  </h3>
                  <div className="h-[300px] w-full relative">
                     {dendro && dendro.icoord && dendro.icoord.length > 0 && (
                       <svg viewBox="0 0 100 100" className="w-full h-full preserve-3d" preserveAspectRatio="none">
                          {(() => {
                            const maxX = Math.max(...dendro.icoord.flat()) || 1;
                            const maxY = Math.max(...dendro.dcoord.flat()) || 1;
                            return dendro.icoord.map((x, i) => (
                              <polyline 
                                 key={i}
                                 points={x.map((xval, idx) => `${xval/maxX*100},${100 - dendro.dcoord[i][idx]/maxY*100}`).join(' ')}
                                 fill="none"
                                 stroke="#4f46e5"
                                 strokeWidth="0.5"
                                 opacity="0.6"
                              />
                            ));
                          })()}
                       </svg>
                     )}
                  </div>
                  <p className="text-[10px] text-gray-500 mt-6 uppercase text-center font-black tracking-widest italic opacity-40">Ward-Linkage Tree Projection (Sampled Observations)</p>
               </div>

               {/* Segment Descriptions */}
               <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100">
                  <h3 className="text-lg font-black text-gray-800 mb-8 flex items-center uppercase tracking-tight">
                     <Package className="mr-2 text-indigo-500" size={18}/> Cluster Taxonomy
                  </h3>
                  <div className="space-y-4">
                     <ClusterInfo color="bg-indigo-500" title="Tier 1: Budget Selection" desc="Low price-point vehicles with high fuel efficiency metrics. Dominates the lower X-axis volume." />
                     <ClusterInfo color="bg-emerald-500" title="Tier 2: Enterprise/Mid" desc="Standard performance indices. Represents the statistical average of the current dataset observations." />
                     <ClusterInfo color="bg-orange-500" title="Tier 3: Premium/Performance" desc="High outliers in horsepower and price. Clustered aggressively in higher vector space." />
                  </div>
               </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

function ClusterInfo({ color, title, desc }) {
  return (
    <div className="flex items-start space-x-4 p-5 rounded-3xl bg-gray-50 border border-gray-100 hover:border-indigo-100 transition-colors">
       <div className={`${color} p-2.5 rounded-2xl text-white mt-1 shadow-md`}>
          <ChevronRight size={16} />
       </div>
       <div>
          <h4 className="text-sm font-black text-gray-800 mb-1">{title}</h4>
          <p className="text-xs text-gray-500 font-medium leading-relaxed">{desc}</p>
       </div>
    </div>
  );
}
