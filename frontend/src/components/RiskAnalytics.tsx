import React from 'react';
import { TrendingUp, TrendingDown, AlertTriangle, ShieldCheck, BrainCircuit } from 'lucide-react';

export const RiskAnalytics: React.FC = () => {
  return (
    <div className="p-8 space-y-8 bg-gray-50/50 dark:bg-gray-950 min-h-screen">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Risk Analytics</h1>
        <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mt-1">AI-driven insights and predictive modeling.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 p-6 rounded-3xl text-white shadow-lg shadow-indigo-500/20">
          <div className="flex justify-between items-start mb-4">
            <div className="p-2 bg-white/20 rounded-xl backdrop-blur-sm">
              <BrainCircuit size={24} />
            </div>
            <span className="flex items-center gap-1 text-sm font-bold bg-white/20 px-2 py-1 rounded-lg backdrop-blur-sm">
              <TrendingDown size={16} /> 14%
            </span>
          </div>
          <h3 className="text-3xl font-bold mb-1">86%</h3>
          <p className="text-indigo-100 font-medium text-sm">Overall Prediction Accuracy</p>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <div className="p-2 bg-rose-50 dark:bg-rose-900/20 text-rose-600 dark:text-rose-400 rounded-xl">
              <AlertTriangle size={24} />
            </div>
            <span className="flex items-center gap-1 text-sm font-bold text-rose-600 bg-rose-50 dark:bg-rose-900/20 px-2 py-1 rounded-lg">
              <TrendingUp size={16} /> 5%
            </span>
          </div>
          <h3 className="text-3xl font-bold text-gray-900 dark:text-gray-100">24</h3>
          <p className="text-gray-500 font-medium text-sm mt-1">False Positives Prevented</p>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <div className="p-2 bg-teal-50 dark:bg-teal-900/20 text-teal-600 dark:text-teal-400 rounded-xl">
              <ShieldCheck size={24} />
            </div>
            <span className="flex items-center gap-1 text-sm font-bold text-teal-600 bg-teal-50 dark:bg-teal-900/20 px-2 py-1 rounded-lg">
              <TrendingUp size={16} /> 12%
            </span>
          </div>
          <h3 className="text-3xl font-bold text-gray-900 dark:text-gray-100">92%</h3>
          <p className="text-gray-500 font-medium text-sm mt-1">Intervention Success Rate</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white dark:bg-gray-900 p-8 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm">
          <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100 mb-6">Trigger Distribution</h2>
          <div className="space-y-6">
            {[
              { label: 'Linguistic Fragmentation', value: 45, color: 'rose' },
              { label: 'Anomalous Latency', value: 30, color: 'orange' },
              { label: 'Motor Echo Delay', value: 15, color: 'indigo' },
              { label: 'Other Indicators', value: 10, color: 'teal' },
            ].map((item, i) => (
              <div key={i}>
                <div className="flex justify-between text-sm font-semibold mb-2">
                  <span className="text-gray-700 dark:text-gray-300">{item.label}</span>
                  <span className="text-gray-900 dark:text-gray-100">{item.value}%</span>
                </div>
                <div className="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-3 overflow-hidden">
                  <div className={`bg-${item.color}-500 h-full rounded-full`} style={{ width: `${item.value}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-8 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm">
          <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100 mb-6">Risk Trajectory (30 Days)</h2>
          <div className="h-64 relative flex items-end justify-between pt-10">
            {/* Simulated line chart area */}
            <div className="absolute inset-0 flex flex-col justify-between pb-6">
              {[100, 75, 50, 25, 0].map((val, i) => (
                <div key={i} className="w-full border-t border-gray-100 dark:border-gray-800/50 flex items-center">
                  <span className="absolute -left-2 -translate-x-full text-[10px] font-semibold text-gray-400">{val}</span>
                </div>
              ))}
            </div>
            
            {/* Bars */}
            <div className="relative z-10 w-full flex justify-between items-end h-full pb-6 px-2">
              {[30, 40, 35, 50, 45, 60, 55, 70, 65, 80, 75, 90].map((h, i) => (
                <div key={i} className="w-4 bg-indigo-500/20 hover:bg-indigo-500 transition-colors rounded-t-md relative group cursor-pointer" style={{ height: `${h}%` }}>
                  <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs font-bold py-1 px-2 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
                    {h}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
