import React from 'react';
import { Search, Filter, MoreVertical, Phone, Mail, Activity } from 'lucide-react';

export const PatientProfiles: React.FC = () => {
  const patients = [
    { id: 'PAT-9921', name: 'Eleanor Vance', age: 42, status: 'Critical', condition: 'Linguistic Fragmentation', image: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=150&h=150' },
    { id: 'PAT-8812', name: 'Marcus Chen', age: 58, status: 'Elevated', condition: 'Anomalous Latency', image: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&q=80&w=150&h=150' },
    { id: 'PAT-4401', name: 'Sarah Jenkins', age: 31, status: 'Stable', condition: 'Baseline Nominal', image: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=150&h=150' },
    { id: 'PAT-1152', name: 'David Miller', age: 64, status: 'Critical', condition: 'Motor Echo Delay', image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=150&h=150' },
    { id: 'PAT-3392', name: 'Priya Patel', age: 29, status: 'Stable', condition: 'Routine Observation', image: 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&q=80&w=150&h=150' },
    { id: 'PAT-7741', name: 'James Wilson', age: 51, status: 'Elevated', condition: 'Elevated Heart Rate', image: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=150&h=150' },
  ];

  return (
    <div className="p-8 space-y-8 bg-gray-50/50 dark:bg-gray-950 min-h-screen">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Patient Profiles</h1>
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mt-1">Manage and monitor your active patients.</p>
        </div>
        
        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
            <input 
              type="text" 
              className="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-full pl-11 pr-5 py-2.5 text-sm focus:ring-2 focus:ring-indigo-500/20 outline-none transition-all shadow-sm" 
              placeholder="Search patients..." 
            />
          </div>
          <button className="p-2.5 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 text-gray-600 dark:text-gray-300 rounded-full hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors shadow-sm">
            <Filter size={20} />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {patients.map((patient) => (
          <div key={patient.id} className="bg-white dark:bg-gray-900 rounded-3xl p-6 border border-gray-100 dark:border-gray-800 shadow-sm hover:shadow-md transition-shadow group">
            <div className="flex justify-between items-start mb-4">
              <span className={`px-3 py-1 text-xs font-bold rounded-full ${
                patient.status === 'Critical' ? 'bg-rose-50 text-rose-600 dark:bg-rose-900/20 dark:text-rose-400' :
                patient.status === 'Elevated' ? 'bg-orange-50 text-orange-600 dark:bg-orange-900/20 dark:text-orange-400' :
                'bg-teal-50 text-teal-600 dark:bg-teal-900/20 dark:text-teal-400'
              }`}>
                {patient.status}
              </span>
              <button className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors">
                <MoreVertical size={20} />
              </button>
            </div>
            
            <div className="flex flex-col items-center text-center mb-6">
              <div className="relative mb-4">
                <img src={patient.image} alt={patient.name} className="w-20 h-20 rounded-full object-cover border-4 border-white dark:border-gray-900 shadow-md" referrerPolicy="no-referrer" />
                <div className={`absolute bottom-0 right-0 w-4 h-4 rounded-full border-2 border-white dark:border-gray-900 ${
                  patient.status === 'Critical' ? 'bg-rose-500' :
                  patient.status === 'Elevated' ? 'bg-orange-500' :
                  'bg-teal-500'
                }`}></div>
              </div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">{patient.name}</h3>
              <p className="text-sm font-medium text-gray-500 mb-2">{patient.id} • {patient.age} yrs</p>
              <div className="flex items-center gap-1.5 text-xs font-semibold text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/20 px-3 py-1.5 rounded-full">
                <Activity size={14} />
                {patient.condition}
              </div>
            </div>

            <div className="flex gap-3 pt-4 border-t border-gray-100 dark:border-gray-800">
              <button className="flex-1 flex items-center justify-center gap-2 py-2.5 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 text-sm font-semibold rounded-xl transition-colors">
                <Mail size={16} />
                Message
              </button>
              <button className="flex-1 flex items-center justify-center gap-2 py-2.5 bg-indigo-50 dark:bg-indigo-900/20 hover:bg-indigo-100 dark:hover:bg-indigo-900/40 text-indigo-700 dark:text-indigo-400 text-sm font-semibold rounded-xl transition-colors">
                <Phone size={16} />
                Call
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
