import { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileType, CheckCircle, Database, Table as TableIcon, Info } from 'lucide-react';
import { uploadDataset } from '../services/api';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
      setError(null);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const data = await uploadDataset(file);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 pb-24">
      <div className="mb-8 p-8 bg-gradient-to-br from-indigo-600 to-blue-700 rounded-[2rem] shadow-xl text-white relative overflow-hidden">
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-3 tracking-tight">Upload Car Dataset</h1>
          <p className="text-blue-100 max-w-2xl text-lg leading-relaxed">
            Initialize your machine learning journey by importing your automobile data. 
            We support CSV and TXT formats for seamless processing.
          </p>
        </div>
        <div className="absolute top-1/2 right-0 -translate-y-1/2 opacity-10 blur-2xl">
          <Database size={300} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1 space-y-6">
           <div 
            className="border-3 border-dashed border-indigo-100 rounded-3xl p-8 bg-white text-center transition-all hover:border-indigo-300 hover:bg-indigo-50/30 cursor-pointer shadow-sm relative group"
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
          >
            <input 
              type="file" 
              accept=".csv,.txt" 
              onChange={handleFileChange} 
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-20"
            />
            <motion.div
              animate={{ y: [0, -12, 0] }}
              transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
              className="mx-auto w-20 h-20 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mb-6 shadow-sm group-hover:bg-indigo-600 group-hover:text-white transition-colors duration-300"
            >
              {file ? <FileType size={40} /> : <Upload size={40} />}
            </motion.div>
            
            <h3 className="text-xl font-bold mb-2 text-gray-800 break-words">
              {file ? file.name : "Select Dataset"}
            </h3>
            <p className="text-gray-500 text-sm mb-6 flex items-center justify-center">
              <Info size={14} className="mr-1"/> {file ? `${(file.size / 1024).toFixed(2)} KB` : "Drop CSV/TXT file here"}
            </p>

            {file && (
              <button 
                onClick={(e) => { e.preventDefault(); e.stopPropagation(); handleUpload(); }}
                disabled={loading}
                className="w-full relative z-30 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-lg transition-all transform hover:-translate-y-1 active:translate-y-0 flex items-center justify-center space-x-2 disabled:opacity-50"
              >
                {loading ? (
                  <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }} className="border-2 border-white border-t-transparent rounded-full w-5 h-5" />
                ) : (
                  <Database size={20} />
                )}
                <span>{loading ? "Processing..." : "Initialize Pipeline"}</span>
              </button>
            )}
          </div>

          {result && (
            <motion.div 
              initial={{ opacity: 0, x: -20 }} 
              animate={{ opacity: 1, x: 0 }}
              className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm space-y-4"
            >
               <h4 className="text-sm font-bold text-gray-400 uppercase tracking-widest flex items-center">
                 <Database size={14} className="mr-2"/> Dataset Metrics
               </h4>
               <div className="grid grid-cols-1 gap-3">
                  <div className="bg-indigo-50/50 p-4 rounded-2xl border border-indigo-50">
                    <p className="text-xs text-indigo-500 font-bold uppercase mb-1">Total Observations</p>
                    <p className="text-2xl font-black text-indigo-900">{result.rows.toLocaleString()}</p>
                  </div>
                  <div className="bg-emerald-50/50 p-4 rounded-2xl border border-emerald-50">
                    <p className="text-xs text-emerald-500 font-bold uppercase mb-1">Feature Count</p>
                    <p className="text-2xl font-black text-emerald-900">{result.columns.length}</p>
                  </div>
               </div>
            </motion.div>
          )}
        </div>

        <div className="lg:col-span-3">
          {error && (
            <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="p-4 bg-red-50 text-red-600 rounded-2xl border border-red-100 flex items-center mb-6">
              <Database className="mr-3" /> <span className="font-medium">{error}</span>
            </motion.div>
          )}

          {!result && !error && (
             <div className="h-full min-h-[400px] bg-white border border-gray-100 rounded-[2.5rem] flex flex-col items-center justify-center text-center p-12 shadow-sm border-dashed">
                <div className="bg-gray-50 p-8 rounded-full mb-6">
                  <TableIcon size={64} className="text-gray-300" />
                </div>
                <h3 className="text-2xl font-bold text-gray-800 mb-2">Awaiting Dataset Preview</h3>
                <p className="text-gray-500 max-w-sm mb-0">Upload a file on the left to see the raw structural data table and feature summary.</p>
             </div>
          )}

          {result && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
              <div className="bg-white rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden">
                <div className="p-6 border-b border-gray-50 bg-gray-50/30 flex justify-between items-center">
                  <h3 className="text-xl font-bold text-gray-800 flex items-center">
                    <TableIcon className="mr-2 text-indigo-600" size={20}/> Dataset Preview <span className="ml-3 text-xs font-medium bg-indigo-100 text-indigo-600 px-2 py-1 rounded-full uppercase tracking-tighter">Initial 10 Rows</span>
                  </h3>
                   <div className="flex space-x-2">
                      <div className="w-2 h-2 rounded-full bg-red-300"></div>
                      <div className="w-2 h-2 rounded-full bg-orange-300"></div>
                      <div className="w-2 h-2 rounded-full bg-green-300"></div>
                   </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm text-gray-500">
                    <thead className="text-[10px] text-gray-400 uppercase bg-gray-50/80 font-black">
                      <tr>
                        {result.columns.map(col => (
                          <th key={col} className="py-4 px-6 border-b border-gray-100 tracking-widest">{col}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-50">
                      {result.preview.map((row, i) => (
                        <tr key={i} className="hover:bg-blue-50/30 transition-colors">
                          {result.columns.map(col => (
                            <td key={col} className="py-4 px-6 max-w-[200px] truncate font-medium text-gray-600">
                              {row[col] === null ? <span className="text-red-300 italic">null</span> : String(row[col])}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
              
              <div className="bg-white p-8 rounded-[2rem] border border-gray-100 shadow-sm flex items-start space-x-4">
                  <div className="bg-blue-50 p-3 rounded-2xl text-blue-600 shadow-inner">
                    <CheckCircle size={24} />
                  </div>
                  <div>
                    <h4 className="text-lg font-bold text-gray-800 mb-1">Upload verified!</h4>
                    <p className="text-gray-500 text-sm leading-relaxed">
                      Dataset integrity checks completed. You can now proceed to the <strong>Dashboard Overview</strong> to see global visualizations or <strong>Statistics</strong> for feature distribution analysis.
                    </p>
                  </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
