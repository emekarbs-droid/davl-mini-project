import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  UploadCloud, 
  LayoutDashboard, 
  BarChart2, 
  Filter, 
  TrendingUp, 
  Crosshair, 
  Map, 
  ListChecks, 
  Network 
} from 'lucide-react';

export default function Sidebar() {
  const tabs = [
    { name: 'Upload Dataset', path: '/', icon: UploadCloud },
    { name: 'Dashboard Overview', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Statistics Analysis', path: '/stats', icon: BarChart2 },
    { name: 'Data Preprocessing', path: '/preprocess', icon: Filter },
    { name: 'Regression', path: '/regression', icon: TrendingUp },
    { name: 'Classification', path: '/classification', icon: Crosshair },
    { name: 'PCA', path: '/pca', icon: Map },
    { name: 'Feature Selection', path: '/feature-selection', icon: ListChecks },
    { name: 'Clustering', path: '/clustering', icon: Network },
  ];

  return (
    <div className="w-72 bg-white h-screen border-r border-gray-100 flex flex-col shadow-sm hidden md:flex sticky top-0 overflow-y-auto">
      <div className="p-6">
        <h2 className="text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 tracking-tight">Auto ML Pro</h2>
        <p className="text-xs text-gray-400 mt-1 uppercase tracking-wider font-semibold">Data Pipeline</p>
      </div>
      
      <nav className="flex-1 px-4 space-y-1">
        {tabs.map((tab) => (
          <NavLink
            key={tab.name}
            to={tab.path}
            className={({ isActive }) =>
               `flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 relative group
                ${isActive ? 'text-blue-700 bg-blue-50' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}`
            }
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <motion.div 
                    layoutId="sidebar-active" 
                    className="absolute inset-0 bg-blue-50 rounded-xl" 
                    initial={false} 
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }} 
                  />
                )}
                <tab.icon className={`mr-3 z-10 relative ${isActive ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-500'}`} size={20} />
                <span className="z-10 relative">{tab.name}</span>
              </>
            )}
          </NavLink>
        ))}
      </nav>
      
      <div className="p-6 border-t border-gray-100 mt-auto">
         <div className="bg-gray-50 rounded-xl p-4 text-center">
            <p className="text-xs text-gray-500 font-medium">Pipeline Status</p>
            <div className="flex items-center justify-center mt-2 text-emerald-600 space-x-1">
               <span className="relative flex h-3 w-3">
                 <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                 <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
               </span>
               <span className="text-xs font-bold uppercase tracking-wider">Active</span>
            </div>
         </div>
      </div>
    </div>
  );
}
