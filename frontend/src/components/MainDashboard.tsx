import React from 'react';
import { Users, Activity, Clock, Calendar, ArrowUpRight, ArrowDownRight, CheckCircle2 } from 'lucide-react';

export const MainDashboard: React.FC = () => {
  return (
    <div className="p-8 space-y-8 bg-gray-50/50 dark:bg-gray-950 min-h-screen">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Good morning, Dr. Thorne 👋</h1>
        <p className="text-gray-500 dark:text-gray-400">Here's what's happening with your patients today.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Total Patients', value: '1,248', trend: '+12%', up: true, icon: Users, color: 'indigo' },
          { label: 'Active Alerts', value: '12', trend: '-2%', up: false, icon: Activity, color: 'rose' },
          { label: 'Pending Reviews', value: '8', trend: '+4%', up: true, icon: Clock, color: 'orange' },
          { label: 'Resolved Today', value: '34', trend: '+18%', up: true, icon: CheckCircle2, color: 'teal' },
        ].map((stat, i) => (
          <div key={i} className="bg-white dark:bg-gray-900 p-6 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm flex flex-col gap-4">
            <div className="flex justify-between items-start">
              <div className={`p-3 rounded-2xl bg-${stat.color}-50 dark:bg-${stat.color}-900/20 text-${stat.color}-600 dark:text-${stat.color}-400`}>
                <stat.icon size={24} />
              </div>
              <span className={`flex items-center gap-1 text-sm font-semibold ${stat.up ? 'text-teal-600' : 'text-rose-600'}`}>
                {stat.trend}
                {stat.up ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
              </span>
            </div>
            <div>
              <h3 className="text-3xl font-bold text-gray-900 dark:text-gray-100">{stat.value}</h3>
              <p className="text-sm font-medium text-gray-500 mt-1">{stat.label}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white dark:bg-gray-900 p-8 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100">Weekly Risk Overview</h2>
            <select className="bg-gray-50 dark:bg-gray-800 border-none text-sm font-semibold text-gray-600 dark:text-gray-300 rounded-full px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option>This Week</option>
              <option>Last Week</option>
            </select>
          </div>
          <div className="h-64 flex items-end justify-between gap-2">
            {[40, 60, 45, 80, 55, 90, 30].map((h, i) => (
              <div key={i} className="w-full flex flex-col justify-end gap-2 group">
                <div className="w-full bg-indigo-100 dark:bg-indigo-900/30 rounded-t-xl relative overflow-hidden transition-all duration-300 group-hover:bg-indigo-200 dark:group-hover:bg-indigo-800/50" style={{ height: `${h}%` }}>
                  <div className="absolute bottom-0 left-0 right-0 bg-indigo-500 rounded-t-xl transition-all duration-500" style={{ height: `${h * 0.7}%` }}></div>
                </div>
                <span className="text-center text-xs font-semibold text-gray-400">
                  {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i]}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-8 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100">Upcoming Schedule</h2>
            <button className="p-2 text-indigo-600 bg-indigo-50 dark:bg-indigo-900/20 rounded-full hover:bg-indigo-100 transition-colors">
              <Calendar size={18} />
            </button>
          </div>
          <div className="space-y-6">
            {[
              { time: '09:00 AM', title: 'Clinical Review Board', type: 'Meeting' },
              { time: '10:30 AM', title: 'Patient Consult: #PAT-8812', type: 'Consultation' },
              { time: '01:00 PM', title: 'Triage Protocol Update', type: 'Administrative' },
              { time: '03:15 PM', title: 'Emergency Escalation Check', type: 'Review' },
            ].map((event, i) => (
              <div key={i} className="flex gap-4 relative">
                <div className="flex flex-col items-center">
                  <div className="w-3 h-3 rounded-full bg-indigo-500 ring-4 ring-indigo-50 dark:ring-indigo-900/20 z-10"></div>
                  {i !== 3 && <div className="w-0.5 h-full bg-gray-100 dark:bg-gray-800 absolute top-3"></div>}
                </div>
                <div className="pb-6">
                  <p className="text-xs font-bold text-indigo-500 mb-1">{event.time}</p>
                  <p className="text-sm font-bold text-gray-900 dark:text-gray-100">{event.title}</p>
                  <p className="text-xs font-medium text-gray-500">{event.type}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
