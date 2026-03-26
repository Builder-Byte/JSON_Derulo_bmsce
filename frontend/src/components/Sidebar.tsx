import React from 'react';
import { 
  LayoutDashboard, 
  Activity, 
  Users, 
  BarChart3, 
  AlertCircle, 
  Settings, 
  HelpCircle, 
  Plus,
  HeartPulse
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, onTabChange }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'triage', label: 'Triage Matrix', icon: Activity },
    { id: 'patients', label: 'Patient Profiles', icon: Users },
    { id: 'analytics', label: 'Risk Analytics', icon: BarChart3 },
    { id: 'escalations', label: 'Escalations', icon: AlertCircle },
  ];

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-white dark:bg-gray-900 border-r border-gray-100 dark:border-gray-800 z-50 flex flex-col">
      <div className="px-6 py-8">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-indigo-100 dark:bg-indigo-900/50 rounded-2xl flex items-center justify-center text-indigo-600 dark:text-indigo-400">
            <HeartPulse size={24} strokeWidth={2.5} />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-gray-900 dark:text-gray-100">Lumen Care</h1>
            <p className="text-[0.65rem] uppercase tracking-wider text-gray-500 font-semibold">Clinical Triage</p>
          </div>
        </div>

        <button className="w-full bg-indigo-500 hover:bg-indigo-600 text-white text-sm font-semibold py-3 px-4 rounded-full mb-8 flex items-center justify-center gap-2 transition-all active:scale-95 shadow-md shadow-indigo-500/20">
          <Plus size={18} />
          New Assessment
        </button>

        <nav className="space-y-2">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-2xl transition-all ${
                activeTab === item.id 
                  ? 'text-indigo-700 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/20' 
                  : 'text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50 hover:text-gray-900 dark:hover:text-gray-100'
              }`}
            >
              <item.icon size={20} strokeWidth={activeTab === item.id ? 2.5 : 2} />
              {item.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="mt-auto p-6 space-y-2">
        <a href="#" className="flex items-center gap-3 px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50 hover:text-gray-900 dark:hover:text-gray-100 rounded-2xl transition-all">
          <Settings size={20} />
          Settings
        </a>
        <a href="#" className="flex items-center gap-3 px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50 hover:text-gray-900 dark:hover:text-gray-100 rounded-2xl transition-all">
          <HelpCircle size={20} />
          Support
        </a>

        <div className="pt-6 flex items-center gap-3 mt-2">
          <img 
            src="https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&q=80&w=100&h=100" 
            alt="Dr. Aris Thorne" 
            className="w-10 h-10 rounded-full border-2 border-white dark:border-gray-800 shadow-sm object-cover"
            referrerPolicy="no-referrer"
          />
          <div className="overflow-hidden text-left">
            <p className="text-sm font-bold text-gray-900 dark:text-gray-100 truncate">Dr. Aris Thorne</p>
            <p className="text-xs text-gray-500 truncate">Chief Medical Officer</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
