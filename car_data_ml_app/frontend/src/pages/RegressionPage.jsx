import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { trainRegression } from '../services/api';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, 
  ResponsiveContainer, ScatterChart, Scatter, BarChart, Bar, Cell, ReferenceLine 
} from 'recharts';
import { 
  Play, TrendingUp, AlertCircle, Award, Target, Info, 
  ChevronRight, ArrowRight, Layers, Database, Activity 
} from 'lucide-react';

const COLORS = ['#4f46e5', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

export default function RegressionPage() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [modelType, setModelType] = useState('linear');

  const handleTrain = async () => {
    setLoading(true);
    try {
      const res = await trainRegression({
        model_type: modelType,
        target: 'price',
        features: [] 
      });
      setData(res);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
    setLoading(false);
  };

  const isOverfit = data && (data.metrics.r2 > 0.98);
  const isUnderfit = data && (data.metrics.r2 < 0.3);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-8 pb-32 max-w-7xl mx-auto space-y-10">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-black text-gray-900 flex items-center">
            <TrendingUp className="mr-3 text-indigo-600" size={32} /> Regression Analysis
          </h1>
          <p className="text-gray-500 mt-1 pl-11">Predict continuous car pricing values based on non-linear physical coefficients.</p>
        </div>
        <div className="flex space-x-3 bg-white p-2 rounded-3xl shadow-sm border border-gray-100">
           {['linear', 'polynomial', 'ridge', 'lasso'].map(m => (
              <button 
                key={m}
                onClick={() => setModelType(m)}
                className={`px-4 py-2 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all ${modelType === m ? 'bg-indigo-600 text-white shadow-lg' : 'text-gray-400 hover:bg-gray-50'}`}
              >
                {m}
              </button>
           ))}
           <div className="w-px bg-gray-100 mx-1 my-1"></div>
           <button 
              onClick={handleTrain} 
              disabled={loading}
              className="px-6 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-2xl shadow-lg flex items-center transition-all disabled:opacity-50 text-[10px] font-black uppercase tracking-widest"
            >
              {loading ? <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }} className="mr-2 border-2 border-white border-t-transparent rounded-full w-3 h-3" /> : <Play size={14} className="mr-2" />}
              Run Engine
            </button>
        </div>
      </header>

      {error && (
        <div className="p-4 bg-red-50 text-red-600 rounded-3xl border border-red-100 flex items-center">
          <AlertCircle className="mr-3" /> <span className="font-bold">{error}</span>
        </div>
      )}

      <AnimatePresence mode="wait">
        {!data && !error ? (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-[500px] bg-white border border-dashed border-gray-200 rounded-[3rem] flex flex-col items-center justify-center text-center p-12">
            <div className="bg-indigo-50 p-10 rounded-full mb-6 text-indigo-200">
              <Layers size={64} />
            </div>
            <h3 className="text-2xl font-black text-gray-800 mb-2">Algorithm Ready</h3>
            <p className="text-gray-500 max-w-sm">Select a model architecture above and initialize the training weights to generate predictive price plots.</p>
          </motion.div>
        ) : data && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-10">
            {/* Global Metrics Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricItem label="R² Accuracy" value={((data?.metrics?.r2 || 0) * 100).toFixed(2) + '%'} icon={Target} color="text-indigo-600" bg="bg-indigo-50" />
                <MetricItem label="Adj. R²" value={((data?.metrics?.adjusted_r2 || 0) * 100).toFixed(2) + '%'} icon={Award} color="text-emerald-600" bg="bg-emerald-50" />
                <MetricItem label="Mean Absolute Error" value={Math.round(data?.metrics?.mae || 0).toLocaleString()} icon={Activity} color="text-orange-600" bg="bg-orange-50" />
                <MetricItem label="Error (RMSE)" value={Math.round(data?.metrics?.rmse || 0).toLocaleString()} icon={Info} color="text-red-600" bg="bg-red-50" />
            </div>

            {/* FITTING INDICATOR */}
            {(isOverfit || isUnderfit) && (
              <div className={`p-6 rounded-[2.5rem] flex items-center space-x-4 border ${isOverfit ? 'bg-red-50 border-red-100 text-red-800' : 'bg-orange-50 border-orange-100 text-orange-800'}`}>
                 <div className={`p-3 rounded-2xl ${isOverfit ? 'bg-red-500' : 'bg-orange-500'} text-white`}>
                    <AlertCircle size={24}/>
                 </div>
                 <div>
                    <h4 className="text-lg font-black uppercase tracking-tight">Warning: {isOverfit ? 'Overfitting' : 'Underfitting'} Detected</h4>
                    <p className="text-sm opacity-80">{isOverfit ? 'The model is memorizing noise. R² is suspiciously high. Try Ridge/Lasso regularization.' : 'The model is too simple for this data. Try a Polynomial architecture.'}</p>
                 </div>
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
               {/* Main Prediction Trend */}
               <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100">
                  <header className="flex justify-between items-center mb-8">
                     <h3 className="text-lg font-black text-gray-800 flex items-center"><TrendingUp size={18} className="mr-2 text-indigo-500"/> Actual vs Predicted</h3>
                     <span className="text-[10px] font-black text-indigo-400 bg-indigo-50 px-3 py-1 rounded-full uppercase">Sample Trace</span>
                  </header>
                  <div className="h-[350px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={data.plot_data}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                        <XAxis dataKey="actual" hide />
                        <YAxis axisLine={false} tickLine={false} tick={{fontSize: 10, fill: '#9ca3af'}} />
                        <Tooltip contentStyle={{borderRadius: '20px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)'}} />
                        <Legend verticalAlign="top" height={36}/>
                        <Line type="monotone" dataKey="actual" stroke="#10b981" strokeWidth={3} dot={false} animateDuration={1500} name="Real Price" />
                        <Line type="monotone" dataKey="predicted" stroke="#4f46e5" strokeWidth={3} dot={{r: 4, fill: '#4f46e5'}} animateDuration={2000} name="Model Prediction" />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
               </div>

               {/* Residual Table */}
               <div className="bg-gray-900 p-8 rounded-[2.5rem] shadow-xl text-white">
                  <header className="flex justify-between items-center mb-8">
                     <h3 className="text-lg font-black flex items-center font-mono tracking-tight"><Database size={18} className="mr-2 text-indigo-400"/> Residual Variance Map</h3>
                     <Info size={16} className="text-gray-500" />
                  </header>
                   <div className="h-[350px]">
                       <ResponsiveContainer width="100%" height="100%">
                          <ScatterChart>
                             <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
                             <XAxis type="number" dataKey="predicted" name="Predicted" axisLine={false} tick={false} />
                             <YAxis type="number" dataKey="residual" name="Residual" axisLine={false} tickLine={false} tick={{fontSize: 10, fill: '#64748b'}} />
                             <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{backgroundColor: '#0f172a', border: 'none', borderRadius: '16px'}} />
                             <Scatter name="Residuals" data={(data?.plot_data || []).map(p => ({...p, residual: (p.actual || 0) - (p.predicted || 0)}))} fill="#6366f1">
                                {(data?.plot_data || []).map((entry, index) => (
                                   <Cell key={`cell-${index}`} fill={(entry.actual - entry.predicted) > 0 ? '#10b981' : '#f43f5e'} />
                                ))}
                             </Scatter>
                             {/* Zero baseline using ReferenceLine which is the correct component for ScatterChart */}
                             <ReferenceLine y={0} stroke="#ffffff" strokeDasharray="5 5" opacity={0.3} />
                          </ScatterChart>
                       </ResponsiveContainer>
                   </div>
                   <p className="text-[10px] text-gray-500 mt-4 uppercase text-center font-black tracking-widest">Random Errors should cluster around zero</p>
               </div>
            </div>

            {/* Feature Importance */}
            <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100">
               <h3 className="text-lg font-black text-gray-800 mb-8 flex items-center uppercase tracking-widest">
                  <Play className="mr-2 text-indigo-500" size={16}/> Regression Coefficients (Beta Weights)
               </h3>
               <div className="h-[300px]">
                   <ResponsiveContainer width="100%" height="100%">
                     <BarChart data={data?.feature_importance || []} layout="vertical">
                       <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f3f4f6" />
                       <XAxis type="number" axisLine={false} tickLine={false} tick={{fontSize: 10}} />
                       <YAxis type="category" dataKey="feature" width={100} axisLine={false} tickLine={false} tick={{fontSize: 10, fontWeight: 'bold'}} />
                       <Tooltip />
                       <Bar dataKey="weight" fill="#4f46e5" radius={[0, 6, 6, 0]}>
                          {(data?.feature_importance || []).map((v, i) => (
                             <Cell key={i} fill={v.weight > 0 ? '#4f46e5' : '#f43f5e'} />
                          ))}
                       </Bar>
                     </BarChart>
                   </ResponsiveContainer>
               </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

function MetricItem({ label, value, icon: Icon, color, bg }) {
  return (
    <div className="bg-white p-6 rounded-[2rem] shadow-sm border border-gray-100 flex items-center space-x-4">
      <div className={`${bg} ${color} p-4 rounded-2xl`}>
        <Icon size={24} />
      </div>
      <div>
        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">{label}</p>
        <p className="text-2xl font-black text-gray-800">{value}</p>
      </div>
    </div>
  );
}
