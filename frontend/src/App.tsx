import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { TopBar } from './components/TopBar';
import { Dashboard as TriageMatrix } from './components/Dashboard';
import { MainDashboard } from './components/MainDashboard';
import { PatientProfiles } from './components/PatientProfiles';
import { RiskAnalytics } from './components/RiskAnalytics';
import { Escalations } from './components/Escalations';
import { Footer } from './components/Footer';
import { HeartPulse } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <MainDashboard />;
      case 'triage':
        return <TriageMatrix />;
      case 'patients':
        return <PatientProfiles />;
      case 'analytics':
        return <RiskAnalytics />;
      case 'escalations':
        return <Escalations />;
      default:
        return <MainDashboard />;
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-50/50 dark:bg-gray-950 font-sans selection:bg-indigo-100 selection:text-indigo-900">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      
      <main className="flex-1 ml-64 flex flex-col min-h-screen">
        <TopBar />
        
        <div className="flex-1">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {renderContent()}
            </motion.div>
          </AnimatePresence>
        </div>

        <Footer />
      </main>

      {/* Floating Action Button */}
      <button className="fixed bottom-10 right-10 w-14 h-14 bg-indigo-500 text-white rounded-full shadow-xl shadow-indigo-500/30 flex items-center justify-center hover:scale-110 active:scale-95 transition-transform z-50 group">
        <HeartPulse size={24} strokeWidth={2.5} />
        <span className="absolute right-full mr-4 bg-gray-900 text-white text-xs py-2 px-4 rounded-xl whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity font-semibold shadow-lg">
          Immediate Assessment
        </span>
      </button>
    </div>
  );
}
