import React from 'react';
import { Patient, Alert } from '../types';
import { Activity, Heart, ShieldAlert, CheckCircle2 } from 'lucide-react';

const patients: Patient[] = [
  { id: '#PAT-9921', riskScore: 94.2, trend: [30, 45, 40, 80, 100], primaryTrigger: 'Linguistic Fragmentation', csi: 0.89, protocol: 'Acute-7 (Critical)', status: 'critical' },
  { id: '#PAT-8812', riskScore: 62.8, trend: [60, 55, 65, 70, 65], primaryTrigger: 'Anomalous Latency', csi: 0.44, protocol: 'Monitor-B', status: 'elevated' },
  { id: '#PAT-4401', riskScore: 12.1, trend: [20, 15, 22, 18, 12], primaryTrigger: 'Baseline Nominal', csi: 0.08, protocol: 'Routine-1', status: 'normal' },
  { id: '#PAT-1152', riskScore: 88.5, trend: [40, 50, 85, 90, 95], primaryTrigger: 'Motor Echo Delay', csi: 0.76, protocol: 'Acute-3 (Obs)', status: 'critical' },
];

const alerts: Alert[] = [
  { id: '1', type: 'critical', time: '2m ago', subjectId: '#9921', title: 'Linguistic Break', message: 'Pattern detected in last audio telemetry window.' },
  { id: '2', type: 'elevated', time: '14m ago', subjectId: '#8812', title: 'Spike in CSI', message: 'Threshold exceeded (0.44 > 0.35 baseline).' },
];

export const Dashboard: React.FC = () => {
  return (
    <div className="p-8 space-y-8 bg-gray-50/50 dark:bg-gray-950 min-h-screen">
      {/* Global Risk Distribution */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-rose-50 dark:bg-rose-900/10 p-6 rounded-3xl border border-rose-100 dark:border-rose-900/30 flex flex-col justify-between shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-rose-200/50 dark:bg-rose-900/50 rounded-xl text-rose-600 dark:text-rose-400">
              <ShieldAlert size={20} />
            </div>
            <span className="text-sm font-semibold text-rose-900 dark:text-rose-300">Critical State</span>
          </div>
          <div className="flex items-baseline gap-3">
            <span className="text-4xl font-bold text-rose-600 dark:text-rose-400">12</span>
            <span className="text-sm text-rose-600/70 dark:text-rose-400/70 font-medium bg-rose-200/30 dark:bg-rose-900/30 px-2 py-1 rounded-lg">+2 since last shift</span>
          </div>
        </div>
        
        <div className="bg-orange-50 dark:bg-orange-900/10 p-6 rounded-3xl border border-orange-100 dark:border-orange-900/30 flex flex-col justify-between shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-orange-200/50 dark:bg-orange-900/50 rounded-xl text-orange-600 dark:text-orange-400">
              <Activity size={20} />
            </div>
            <span className="text-sm font-semibold text-orange-900 dark:text-orange-300">Elevated Risk</span>
          </div>
          <div className="flex items-baseline gap-3">
            <span className="text-4xl font-bold text-orange-600 dark:text-orange-400">48</span>
            <span className="text-sm text-orange-600/70 dark:text-orange-400/70 font-medium bg-orange-200/30 dark:bg-orange-900/30 px-2 py-1 rounded-lg">-5 resolving</span>
          </div>
        </div>

        <div className="bg-teal-50 dark:bg-teal-900/10 p-6 rounded-3xl border border-teal-100 dark:border-teal-900/30 flex flex-col justify-between shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-teal-200/50 dark:bg-teal-900/50 rounded-xl text-teal-600 dark:text-teal-400">
              <CheckCircle2 size={20} />
            </div>
            <span className="text-sm font-semibold text-teal-900 dark:text-teal-300">Normal Baseline</span>
          </div>
          <div className="flex items-baseline gap-3">
            <span className="text-4xl font-bold text-teal-600 dark:text-teal-400">194</span>
            <span className="text-sm text-teal-600/70 dark:text-teal-400/70 font-medium bg-teal-200/30 dark:bg-teal-900/30 px-2 py-1 rounded-lg">Stable volume</span>
          </div>
        </div>
      </section>

      <div className="grid grid-cols-12 gap-8">
        {/* Triage Table */}
        <div className="col-span-12 xl:col-span-8 bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 shadow-sm shadow-gray-200/40 dark:shadow-none overflow-hidden rounded-3xl">
          <div className="px-8 py-6 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center">
            <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">Active Subject Triage</h3>
            <div className="flex gap-2">
              <span className="px-3 py-1 bg-teal-50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400 text-xs font-semibold rounded-full flex items-center gap-2">
                <span className="w-2 h-2 bg-teal-500 rounded-full animate-pulse"></span>
                Real-time Stream Active
              </span>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-gray-100 dark:border-gray-800">
                  <th className="px-8 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">Subject ID</th>
                  <th className="px-8 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">Risk Score</th>
                  <th className="px-8 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">Trend</th>
                  <th className="px-8 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">Primary Trigger</th>
                  <th className="px-8 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider text-center">CSI</th>
                  <th className="px-8 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50 dark:divide-gray-800/50">
                {patients.map((patient) => (
                  <tr 
                    key={patient.id} 
                    className={`hover:bg-gray-50/80 dark:hover:bg-gray-800/30 transition-colors cursor-pointer group`}
                  >
                    <td className="px-8 py-5 text-sm font-bold text-gray-900 dark:text-gray-100">{patient.id}</td>
                    <td className="px-8 py-5">
                      <div className="flex items-center gap-2.5">
                        <div className={`w-2 h-2 rounded-full ${
                          patient.status === 'critical' ? 'bg-rose-500 animate-pulse shadow-[0_0_8px_rgba(244,63,94,0.6)]' : 
                          patient.status === 'elevated' ? 'bg-orange-400' : 'bg-teal-400'
                        }`}></div>
                        <span className={`text-base font-bold ${
                          patient.status === 'critical' ? 'text-rose-600 dark:text-rose-400' : 
                          patient.status === 'elevated' ? 'text-orange-600 dark:text-orange-400' : 'text-teal-600 dark:text-teal-400'
                        }`}>{patient.riskScore}</span>
                      </div>
                    </td>
                    <td className="px-8 py-5">
                      <div className="w-24 h-8 flex items-end gap-1">
                        {patient.trend.map((val, i) => (
                          <div 
                            key={i} 
                            className={`flex-1 rounded-t-sm transition-all duration-300 group-hover:opacity-100 ${
                              patient.status === 'critical' ? 'bg-rose-500' : 
                              patient.status === 'elevated' ? 'bg-orange-400' : 'bg-teal-400'
                            }`} 
                            style={{ height: `${val}%`, opacity: i < 3 ? 0.4 : 0.8 }}
                          ></div>
                        ))}
                      </div>
                    </td>
                    <td className="px-8 py-5">
                      <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                        patient.status === 'critical' ? 'bg-rose-50 dark:bg-rose-900/30 text-rose-700 dark:text-rose-400' : 
                        patient.status === 'elevated' ? 'bg-orange-50 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400' : 
                        'bg-teal-50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-400'
                      }`}>
                        {patient.primaryTrigger}
                      </span>
                    </td>
                    <td className="px-8 py-5 text-center text-sm font-medium text-gray-500 dark:text-gray-400">{patient.csi}</td>
                    <td className="px-8 py-5">
                      <button className={`text-sm font-semibold px-4 py-1.5 rounded-full transition-colors ${
                        patient.status === 'critical' ? 'bg-rose-100 text-rose-700 hover:bg-rose-200 dark:bg-rose-900/40 dark:text-rose-300' : 
                        patient.status === 'elevated' ? 'bg-orange-100 text-orange-700 hover:bg-orange-200 dark:bg-orange-900/40 dark:text-orange-300' : 
                        'bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300'
                      }`}>
                        {patient.status === 'critical' ? 'Escalate' : patient.status === 'elevated' ? 'Monitor' : 'Review'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="p-5 bg-gray-50/50 dark:bg-gray-800/30 border-t border-gray-100 dark:border-gray-800 text-center">
            <button className="text-sm font-semibold text-indigo-600 hover:text-indigo-700 transition-colors">
              Load More Clinical Data
            </button>
          </div>
        </div>

        {/* Sidebar Content */}
        <div className="col-span-12 xl:col-span-4 space-y-8">
          {/* Deep Dive Preview */}
          <div className="bg-indigo-950 text-indigo-50 p-8 rounded-3xl shadow-xl relative overflow-hidden">
            <div className="absolute -top-10 -right-10 p-4 opacity-10 text-indigo-300">
              <Heart size={160} strokeWidth={1} />
            </div>
            <div className="relative z-10">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-14 h-14 bg-rose-500 rounded-2xl flex items-center justify-center font-bold text-2xl text-white shadow-lg shadow-rose-500/30">94</div>
                <div>
                  <p className="text-xs uppercase tracking-wider text-indigo-300 font-semibold mb-1">Focus Subject</p>
                  <h4 className="text-xl font-bold text-white">PAT-9921</h4>
                </div>
              </div>
              
              <div className="space-y-6">
                <div className="bg-indigo-900/50 p-5 rounded-2xl border border-indigo-800/50 backdrop-blur-sm">
                  <div className="flex justify-between text-xs mb-3 font-semibold text-indigo-200 uppercase tracking-wider">
                    <span>Telemetry Spike (24h)</span>
                    <span className="text-rose-400">98th Percentile</span>
                  </div>
                  <div className="h-16 w-full flex items-end gap-1.5">
                    {[20, 30, 25, 70, 90, 100, 85, 40].map((h, i) => (
                      <div 
                        key={i} 
                        className={`flex-1 rounded-sm transition-all duration-500 ${h > 60 ? 'bg-rose-500' : 'bg-indigo-400/40'}`} 
                        style={{ height: `${h}%` }}
                      ></div>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-indigo-900/50 p-4 rounded-2xl border border-indigo-800/50 backdrop-blur-sm">
                    <p className="text-xs text-indigo-300 uppercase tracking-wider font-semibold mb-1">Latency</p>
                    <p className="text-lg font-bold text-white">420ms <span className="text-rose-400 ml-1">↑</span></p>
                  </div>
                  <div className="bg-indigo-900/50 p-4 rounded-2xl border border-indigo-800/50 backdrop-blur-sm">
                    <p className="text-xs text-indigo-300 uppercase tracking-wider font-semibold mb-1">Pulse</p>
                    <p className="text-lg font-bold text-white">112 bpm</p>
                  </div>
                </div>

                <button className="w-full py-3.5 bg-white text-indigo-950 text-sm font-bold rounded-xl hover:bg-indigo-50 transition-colors shadow-lg">
                  View Full Diagnostics
                </button>
              </div>
            </div>
          </div>

          {/* Escalation Queue */}
          <div className="bg-white dark:bg-gray-900 p-6 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-sm font-bold text-gray-900 dark:text-gray-100">Escalation Queue</h3>
              <span className="flex h-3 w-3 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
              </span>
            </div>
            <div className="space-y-4">
              {alerts.map((alert) => (
                <div key={alert.id} className={`p-4 bg-gray-50 dark:bg-gray-800/50 rounded-2xl border border-gray-100 dark:border-gray-700/50 relative overflow-hidden`}>
                  <div className={`absolute left-0 top-0 bottom-0 w-1.5 ${alert.type === 'critical' ? 'bg-rose-500' : 'bg-orange-400'}`}></div>
                  <div className="flex justify-between items-start mb-2 pl-2">
                    <span className={`text-xs font-bold uppercase tracking-wider ${alert.type === 'critical' ? 'text-rose-600 dark:text-rose-400' : 'text-orange-600 dark:text-orange-400'}`}>
                      {alert.type} ALERT
                    </span>
                    <span className="text-xs font-medium text-gray-400">{alert.time}</span>
                  </div>
                  <p className="text-sm font-bold text-gray-900 dark:text-gray-100 pl-2 mb-1">Subject {alert.subjectId}: {alert.title}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 pl-2 leading-relaxed">{alert.message}</p>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};
