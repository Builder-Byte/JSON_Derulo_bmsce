import React from 'react';
import { Cloud } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-auto bg-white dark:bg-gray-900 px-8 py-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-xs font-medium text-gray-500">
      <div className="flex gap-6 items-center">
        <div className="flex items-center gap-2 bg-teal-50 dark:bg-teal-900/20 px-3 py-1.5 rounded-full text-teal-700 dark:text-teal-400">
          <span className="w-2 h-2 rounded-full bg-teal-500 animate-pulse"></span>
          <span className="font-semibold">System Healthy</span>
        </div>
        <div className="flex items-center gap-2">
          <Cloud size={16} />
          <span>Sync: 0.4s Latency</span>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <span>© 2024 Lumen Care</span>
        <span className="text-gray-300 dark:text-gray-700">|</span>
        <span className="font-semibold text-gray-400">Node: DX-991</span>
      </div>
    </footer>
  );
};
