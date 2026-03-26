import React from 'react';
import { Search, Bell, History, Filter } from 'lucide-react';

export const TopBar: React.FC = () => {
  return (
    <header className="sticky top-0 z-40 flex justify-between items-center w-full px-8 py-5 bg-white/80 dark:bg-gray-950/80 backdrop-blur-xl border-b border-gray-100 dark:border-gray-800">
      <div className="flex items-center gap-8">
        <h2 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-gray-100">Clinical Risk Matrix</h2>
        <nav className="hidden lg:flex gap-8 ml-4">
          <a className="text-sm font-semibold text-indigo-600 dark:text-indigo-400 border-b-2 border-indigo-500 pb-1" href="#">All Cases</a>
          <a className="text-sm font-medium text-gray-500 dark:text-gray-400 hover:text-indigo-500 transition-colors" href="#">High Severity</a>
          <a className="text-sm font-medium text-gray-500 dark:text-gray-400 hover:text-indigo-500 transition-colors" href="#">Pending Review</a>
        </nav>
      </div>

      <div className="flex items-center gap-5">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input 
            type="text" 
            className="bg-gray-100 dark:bg-gray-900 border-none rounded-full pl-11 pr-5 py-2.5 text-sm w-72 focus:ring-2 focus:ring-indigo-500/20 focus:bg-white dark:focus:bg-gray-800 outline-none transition-all" 
            placeholder="Search patients or IDs..." 
          />
        </div>
        
        <div className="flex items-center gap-2 border-x border-gray-200 dark:border-gray-800 px-5">
          <button className="p-2.5 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 rounded-full transition-colors relative">
            <Bell size={20} />
            <span className="absolute top-2 right-2 w-2.5 h-2.5 bg-rose-500 rounded-full border-2 border-white dark:border-gray-950"></span>
          </button>
          <button className="p-2.5 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 rounded-full transition-colors">
            <History size={20} />
          </button>
          <button className="p-2.5 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 rounded-full transition-colors">
            <Filter size={20} />
          </button>
        </div>

        <button className="bg-indigo-500 hover:bg-indigo-600 text-white text-sm font-semibold py-2.5 px-6 rounded-full transition-all shadow-md shadow-indigo-500/20">
          Escalate Case
        </button>
      </div>
    </header>
  );
};
