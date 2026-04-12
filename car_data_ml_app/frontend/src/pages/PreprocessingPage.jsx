import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { preprocessData } from '../services/api';
import { 
  Play, Settings, Database, Columns, Filter, CheckCircle2, 
  ArrowRight, ShieldCheck, XCircle, Info, Zap
} from 'lucide-react';

export default function PreprocessingPage() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const [options, setOptions] = useState({
    imputation: 'mean',
    outlier_method: 'iqr',
    encode: true,
    scale: 'standard',
    remove_duplicates: true
  });

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setOptions({ ...options, [e.target.name]: value });
  };

  const handleRun = async () => {
    setLoading(true);
    try {
      const res = await preprocessData(options);
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
             <Filter className="mr-3 text-blue-600" size={32}/> Data Preprocessing
          </h1>
          <p className="text-gray-500 mt-1 pl-11">Configure cleaning strategies and verify transformation integrity.</p>
        </div>
      </header>

      <div className="grid grid-cols-1 xl:grid-cols-4 gap-10">
        {/* Settings Panel */}
        <section className="xl:col-span-1 space-y-6">
          <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 sticky top-8">
            <h3 className="text-xl font-extrabold text-gray-800 mb-8 flex items-center">
              <Settings className="mr-2 text-blue-500" size={20}/> Pipeline Config
            </h3>
            
            <div className="space-y-6">
              <ConfigGroup label="Imputation Strategy" name="imputation" value={options.imputation} onChange={handleChange}>
                <option value="mean">Mean (Averages)</option>
                <option value="median">Median (Mid-point)</option>
              </ConfigGroup>

              <ConfigGroup label="Outlier Clipping" name="outlier_method" value={options.outlier_method} onChange={handleChange}>
                <option value="none">Disabled</option>
                <option value="iqr">IQR Bounds (Standard)</option>
                <option value="z-score">Z-Score (Sigma &gt; 3)</option>
              </ConfigGroup>

              <ConfigGroup label="Feature Scaling" name="scale" value={options.scale} onChange={handleChange}>
                <option value="none">Raw (Untouched)</option>
                <option value="standard">Z-Standardize (0, 1)</option>
                <option value="minmax">Min-Max (0 to 1)</option>
              </ConfigGroup>

              <div className="space-y-4 pt-4 border-t border-gray-50">
                <Toggle label="One-Hot Encode" name="encode" checked={options.encode} onChange={handleChange} />
                <Toggle label="Remove Duplicates" name="remove_duplicates" checked={options.remove_duplicates} onChange={handleChange} />
              </div>

              <button 
                onClick={handleRun} 
                disabled={loading}
                className="w-full mt-6 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl shadow-lg flex items-center justify-center transition-all group disabled:opacity-50 font-black"
              >
                {loading ? <ActivityIcon /> : <Zap size={20} className="mr-2 group-hover:scale-125 transition-transform" />}
                {loading ? "Transforming..." : "Execute Pipeline"}
              </button>
            </div>
          </div>
        </section>

        {/* Results Panel */}
        <section className="xl:col-span-3">
          <AnimatePresence mode="wait">
            {!data && !error ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-full min-h-[500px] bg-white border border-dashed border-gray-200 rounded-[3rem] flex flex-col items-center justify-center text-center p-12">
                 <div className="bg-gray-50 p-10 rounded-full mb-6">
                    <Database size={64} className="text-gray-300" />
                 </div>
                 <h3 className="text-2xl font-black text-gray-800 mb-2">Ready for Transformation</h3>
                 <p className="text-gray-500 max-w-sm">Configure your ML strategies on the left to begin cleaning the car dataset observations.</p>
              </motion.div>
            ) : error ? (
                <div className="p-6 bg-red-50 text-red-600 rounded-3xl border border-red-100 flex items-center shadow-sm">
                  <XCircle className="mr-3 flex-shrink-0" /> <span className="font-bold">{error}</span>
                </div>
            ) : (
              <motion.div initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} className="space-y-8">
                {/* Status Bar */}
                <div className="bg-emerald-50 text-emerald-700 p-8 rounded-[2.5rem] border border-emerald-100 flex items-center justify-between shadow-sm relative overflow-hidden">
                   <div className="flex items-center relative z-10">
                      <div className="bg-emerald-500 text-white p-3 rounded-2xl mr-4 shadow-lg shadow-emerald-200">
                        <ShieldCheck size={28} />
                      </div>
                      <div>
                        <h3 className="text-2xl font-black">Cleaning Successful</h3>
                        <p className="text-emerald-600 opacity-80 text-sm">All selected pipeline stages were applied to the data memory.</p>
                      </div>
                   </div>
                   <motion.div animate={{ opacity: [0.3, 0.6, 0.3] }} transition={{ repeat: Infinity, duration: 3 }} className="absolute -right-10 top-0 text-emerald-100 -rotate-12 translate-y-4">
                      <CheckCircle2 size={160} />
                   </motion.div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                   <MetricBox label="Row Health" oldVal={data.original_rows} newVal={data.new_rows} suffix="Rows" color="bg-blue-500" />
                   <MetricBox label="Feature Map" oldVal={data.original_cols} newVal={data.new_cols} suffix="Cols" color="bg-indigo-500" />
                </div>

                {/* Cleaning Steps Log */}
                <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100">
                   <h3 className="text-lg font-black text-gray-800 mb-8 flex items-center uppercase tracking-widest">
                      <Play className="mr-2 text-blue-500" size={16}/> Pipeline Execution Log
                   </h3>
                   <div className="space-y-4">
                      <LogItem status="success" label="Missing Value Handling" detail={`${options.imputation.toUpperCase()} imputation applied to numerical holes.`} />
                      <LogItem status={options.outlier_method !== 'none' ? 'success' : 'info'} label="Outlier Clipping" detail={options.outlier_method !== 'none' ? `${options.outlier_method.toUpperCase()} method filtered extreme values.` : 'Outlier clipping was bypassed by user.'} />
                      <LogItem status={options.encode ? 'success' : 'info'} label="Categorical Encoding" detail={options.encode ? 'Text-based features flattened into One-Hot numeric vectors.' : 'Maintained raw text categories.'} />
                      <LogItem status={options.scale !== 'none' ? 'success' : 'info'} label="Dimensional Scaling" detail={options.scale !== 'none' ? `${options.scale} scaling normalized feature ranges.` : 'Feature magnitudes were preserved in raw state.'} />
                   </div>
                </div>

                <div className="bg-white rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden">
                  <div className="p-6 border-b border-gray-50 flex justify-between items-center">
                    <h3 className="text-lg font-black text-gray-800">Transformed Data Sample</h3>
                    <span className="text-[10px] font-black text-blue-500 bg-blue-50 px-3 py-1 rounded-full uppercase">Matrix Preview</span>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs text-gray-400">
                      <thead className="bg-gray-50/50 uppercase tracking-widest text-[9px] font-black">
                        <tr>
                          {Object.keys(data.sample[0] || {}).map(key => <th key={key} className="py-4 px-6 border-b border-gray-100 whitespace-nowrap">{key}</th>)}
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-50 text-gray-600 font-medium">
                        {data.sample.map((row, i) => (
                           <tr key={i} className="hover:bg-blue-50/20">
                             {Object.values(row).map((val, j) => <td key={j} className="py-4 px-6 truncate max-w-[150px]">{typeof val === 'number' ? val.toFixed(4) : String(val)}</td>)}
                           </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </section>
      </div>
    </motion.div>
  );
}

function ConfigGroup({ label, name, value, onChange, children }) {
  return (
    <div>
      <label className="block text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2 pl-1 italic">{label}</label>
      <select name={name} value={value} onChange={onChange} className="w-full border-2 border-gray-100 rounded-2xl p-3.5 bg-gray-50 outline-none focus:border-blue-500 focus:bg-white transition-all text-sm font-bold text-gray-700 appearance-none shadow-sm cursor-pointer">
        {children}
      </select>
    </div>
  );
}

function Toggle({ label, name, checked, onChange }) {
  return (
    <div className="flex items-center justify-between p-1">
      <label className="text-sm font-bold text-gray-600 group cursor-pointer flex items-center">
        <input type="checkbox" name={name} checked={checked} onChange={onChange} className="hidden" />
        <div className={`w-10 h-6 rounded-full mr-3 transition-colors flex items-center relative ${checked ? 'bg-blue-600' : 'bg-gray-200'}`}>
          <motion.div animate={{ x: checked ? 18 : 3 }} className="w-4 h-4 bg-white rounded-full shadow-sm" />
        </div>
        {label}
      </label>
    </div>
  );
}

function MetricBox({ label, oldVal, newVal, suffix, color }) {
  return (
    <div className="bg-white p-8 rounded-[2.5rem] border border-gray-100 shadow-sm flex items-center">
       <div className={`${color} p-4 rounded-3xl text-white mr-6 shadow-lg shadow-blue-100`}>
          <ActivityIcon size={24} />
       </div>
       <div className="flex-1">
          <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-2">{label}</p>
          <div className="flex items-center space-x-4">
             <div className="text-xl font-bold text-gray-300 line-through decoration-gray-200">{oldVal}</div>
             <ArrowRight className="text-blue-300" size={16} />
             <div className="text-3xl font-black text-gray-800">{newVal} <span className="text-xs text-gray-400 uppercase font-black">{suffix}</span></div>
          </div>
       </div>
    </div>
  );
}

function LogItem({ status, label, detail }) {
  return (
    <div className="flex items-start space-x-4 p-4 rounded-2xl hover:bg-gray-50 transition-colors">
       {status === 'success' ? <CheckCircle2 className="text-emerald-500 mt-1 flex-shrink-0" size={18} /> : <Info className="text-blue-300 mt-1 flex-shrink-0" size={18} />}
       <div>
          <h4 className={`text-sm font-black ${status === 'success' ? 'text-gray-800' : 'text-gray-400'}`}>{label}</h4>
          <p className="text-xs text-gray-500 font-medium">{detail}</p>
       </div>
    </div>
  );
}

function ActivityIcon({ size = 20 }) {
  return (
    <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }} className="mr-2">
      <Zap size={size} />
    </motion.div>
  );
}
