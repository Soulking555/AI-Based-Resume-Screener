import React, { useState, useEffect } from 'react';

function Dashboard({ onNavigate, onSelectCandidate }) {
  const [stats, setStats] = useState({
    total: 0,
    shortlisted: 0,
    rejected: 0,
    pending: 0
  });
  const [recentCandidates, setRecentCandidates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('http://localhost:8000/api/dashboard/stats').catch(() => ({})),
      fetch('http://localhost:8000/api/candidates').catch(() => [])
    ])
      .then(async ([statsRes, candRes]) => {
        const statsData = statsRes.json ? await statsRes.json() : stats;
        const candData = candRes.json ? await candRes.json() : [];
        setStats(statsData);
        // Show only the 5 most recent candidates on the dashboard
        setRecentCandidates(candData.slice(0, 5));
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch dashboard data", err);
        setLoading(false);
      });
  }, []);

  const handleClearData = async () => {
    if (!window.confirm("Are you sure you want to clear all candidate data and resumes? This action cannot be undone.")) return;
    
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/candidates/clear', { method: 'DELETE' });
      if (res.ok) {
        window.location.reload();
      } else {
        alert("Failed to clear data.");
        setLoading(false);
      }
    } catch (err) {
      console.error(err);
      alert("Error clearing data.");
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <p style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>INITIALIZING AI ENGINE...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="header">
        <div>
          <h1>Talent Command Center</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>AI-driven candidate matching and intelligence reports are ready for review.</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn btn-glass" style={{ color: 'var(--danger)', borderColor: 'var(--danger)' }} onClick={handleClearData}>
            Clear All Data
          </button>
          <button className="btn btn-primary" onClick={() => onNavigate('candidates')}>
            Upload Resume
          </button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-title">Total Applications</div>
          <div className="stat-value">{stats.total}</div>
        </div>
        <div className="stat-card">
          <div className="stat-title" style={{color: 'var(--success)'}}>Shortlisted</div>
          <div className="stat-value">{stats.shortlisted}</div>
        </div>
        <div className="stat-card">
          <div className="stat-title" style={{color: 'var(--danger)'}}>Rejected</div>
          <div className="stat-value">{stats.rejected}</div>
        </div>
        <div className="stat-card">
          <div className="stat-title" style={{color: 'var(--warning)'}}>AI Evaluating</div>
          <div className="stat-value">{stats.pending}</div>
        </div>
      </div>

      <div className="section-title">Recent Candidates</div>
      <div className="candidates-list">
        <table>
          <thead>
            <tr>
              <th>Candidate</th>
              <th>AI Score</th>
              <th>Key Skills</th>
              <th>Cluster</th>
              <th>Applied Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {recentCandidates.map(c => (
              <tr key={c.id}>
                <td style={{ fontWeight: 600, color: 'var(--text-main)' }}>{c.name}</td>
                <td>
                  <span className={`badge ${c.score >= 70 ? 'success' : c.score < 40 ? 'danger' : 'warning'}`}>
                    {c.score}% Match
                  </span>
                </td>
                <td style={{ color: 'var(--text-muted)' }}>
                  {c.skills && c.skills.length > 0 ? c.skills.slice(0, 3).join(", ") : "Analyzing..."}
                </td>
                <td>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--primary-dim)' }}>
                    {c.cluster || 'Unclustered'}
                  </span>
                </td>
                <td style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                  {new Date(c.date).toLocaleDateString()}
                </td>
                <td>
                  <button className="btn btn-glass" style={{ padding: '0.5rem 1rem', fontSize: '0.8rem' }} onClick={() => onSelectCandidate(c)}>
                    View AI Report
                  </button>
                </td>
              </tr>
            ))}
            {recentCandidates.length === 0 && (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                  No candidates found. Upload a resume to begin AI analysis.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;
