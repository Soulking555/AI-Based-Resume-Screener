import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import CandidateList from './components/CandidateList';
import CandidateProfile from './components/CandidateProfile';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  const navigateToCandidate = (candidate) => {
    setSelectedCandidate(candidate);
    setActiveTab('profile');
  };

  return (
    <div className="app-container">
      <div className="sidebar">
        <div className="logo">Aether Talent</div>
        
        <div 
          className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          <span style={{ fontSize: '1.2rem' }}>✦</span> Command Center
        </div>
        
        <div 
          className={`nav-item ${activeTab === 'candidates' ? 'active' : ''}`}
          onClick={() => setActiveTab('candidates')}
        >
          <span style={{ fontSize: '1.2rem' }}>◫</span> Talent Pool
        </div>
        
        {activeTab === 'profile' && selectedCandidate && (
          <div className="nav-item active">
            <span style={{ fontSize: '1.2rem' }}>◉</span> Profile: {selectedCandidate.name.split(' ')[0]}
          </div>
        )}
      </div>
      
      <div className="main-content">
        {activeTab === 'dashboard' && <Dashboard onNavigate={(tab) => setActiveTab(tab)} onSelectCandidate={navigateToCandidate} />}
        {activeTab === 'candidates' && <CandidateList onSelectCandidate={navigateToCandidate} />}
        {activeTab === 'profile' && selectedCandidate && (
          <CandidateProfile candidate={selectedCandidate} />
        )}
      </div>
    </div>
  );
}

export default App;
