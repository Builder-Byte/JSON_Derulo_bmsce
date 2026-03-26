import React from 'react';
import { AlertTriangle, Clock, ArrowRight, User, Phone, CheckCircle2 } from 'lucide-react';

export const Escalations: React.FC = () => {
  const escalations = [
    { id: 'ESC-1092', patient: 'Eleanor Vance', time: '10 mins ago', type: 'Critical', reason: 'Consecutive linguistic breaks detected over 3 sessions.', assignedTo: 'Dr. Thorne' },
    { id: 'ESC-1091', patient: 'David Miller', time: '45 mins ago', type: 'High', reason: 'Motor echo delay threshold exceeded (0.76 > 0.50).', assignedTo: 'Unassigned' },
    { id: 'ESC-1090', patient: 'Marcus Chen', time: '2 hours ago', type: 'Medium', reason: 'Anomalous latency pattern identified.', assignedTo: 'Dr. Sarah Lee' },
  ];

  return (
    <div className="p-8 space-y-8 bg-gray-50/50 dark:bg-gray-950 min-h-screen">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Active Escalations</h1>
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mt-1">Cases requiring immediate clinical review.</p>
        </div>
        <button className="bg-rose-500 hover:bg-rose-600 text-white text-sm font-semibold py-2.5 px-6 rounded-full transition-all shadow-md shadow-rose-500/20 flex items-center gap-2">
          <AlertTriangle size={18} />
          Declare Emergency
        </button>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm overflow-hidden">
        <div className="divide-y divide-gray-100 dark:divide-gray-800">
          {escalations.map((esc, i) => (
            <div key={i} className="p-6 hover:bg-gray-50/50 dark:hover:bg-gray-800/30 transition-colors flex flex-col xl:flex-row gap-6 items-start xl:items-center justify-between">
              
              <div className="flex items-start gap-4 flex-1">
                <div className={`p-3 rounded-2xl mt-1 ${
                  esc.type === 'Critical' ? 'bg-rose-100 text-rose-600 dark:bg-rose-900/30 dark:text-rose-400' :
                  esc.type === 'High' ? 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400' :
                  'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400'
                }`}>
                  <AlertTriangle size={24} />
                </div>
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">{esc.patient}</h3>
                    <span className="text-xs font-bold text-gray-400 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded-md">{esc.id}</span>
                  </div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-300 mb-2">{esc.reason}</p>
                  <div className="flex items-center gap-4 text-xs font-semibold text-gray-500">
                    <span className="flex items-center gap-1.5"><Clock size={14} /> {esc.time}</span>
                    <span className="flex items-center gap-1.5"><User size={14} /> {esc.assignedTo}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3 w-full xl:w-auto">
                <button className="flex-1 xl:flex-none flex items-center justify-center gap-2 px-6 py-3 bg-indigo-50 dark:bg-indigo-900/20 text-indigo-700 dark:text-indigo-400 hover:bg-indigo-100 dark:hover:bg-indigo-900/40 font-semibold text-sm rounded-xl transition-colors">
                  Review Case
                  <ArrowRight size={16} />
                </button>
                <button className="p-3 text-gray-400 hover:text-teal-600 hover:bg-teal-50 dark:hover:bg-teal-900/20 rounded-xl transition-colors" title="Mark as Resolved">
                  <CheckCircle2 size={20} />
                </button>
                <button className="p-3 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 rounded-xl transition-colors" title="Contact Patient">
                  <Phone size={20} />
                </button>
              </div>

            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
