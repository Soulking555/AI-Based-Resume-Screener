import React, { useState, useEffect } from 'react';

function CandidateList({ onSelectCandidate }) {
  const [candidates, setCandidates] = useState([]);
  const [search, setSearch] = useState('');
  const [minScore, setMinScore] = useState(0);

  const [file, setFile] = useState(null);
  const [candidateName, setCandidateName] = useState('');
  const [jobId, setJobId] = useState(1); // MOCK Job ID
  const [jobDescription, setJobDescription] = useState('');
  const [uploading, setUploading] = useState(false);
  const [clustering, setClustering] = useState(false);

  const fetchCandidates = () => {
    fetch(`http://localhost:8000/api/candidates?search=${search}&min_score=${minScore}`)
      .then(res => res.json())
      .then(data => setCandidates(data))
      .catch(err => console.error("Error fetching candidates:", err));
  };

  useEffect(() => {
    fetchCandidates();
  }, [search, minScore]);

  const exportToCSV = () => {
    const headers = ["Name,Score,Cluster,Applied Date"];
    const rows = candidates.map(c => `${c.name},${c.score},${c.cluster || 'Unclustered'},${new Date(c.date).toLocaleDateString()}`);
    const csvContent = "data:text/csv;charset=utf-8," + headers.concat(rows).join("\\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "shortlist.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleCluster = async () => {
    setClustering(true);
    try {
      const res = await fetch('http://localhost:8000/api/cluster', { method: 'POST' });
      if (res.ok) {
        fetchCandidates(); // Refresh list to show new clusters
      } else {
        alert("Failed to run clustering.");
      }
    } catch (err) {
      console.error(err);
      alert("Error contacting the AI Engine.");
    }
    setClustering(false);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file || !candidateName || !jobDescription) {
      alert("Please provide the candidate name, resume, and job description.");
      return;
    }
    
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("candidate_name", candidateName);
    formData.append("job_description", jobDescription);

    try {
      const res = await fetch('http://localhost:8000/api/upload_resume', {
        method: 'POST',
        body: formData
      });
      
      if (res.ok) {
        setFile(null);
        setCandidateName('');
        setJobDescription('');
        fetchCandidates();
      } else {
        alert("Error uploading resume. Check backend logs.");
      }
    } catch (err) {
      console.error(err);
      alert("Error processing upload.");
    }
    setUploading(false);
  };

  return (
    <div>
      <div className="header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <div>
          <h1>Talent Pool</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>Manage and rank applicants</p>
        </div>
      </div>

      <div className="upload-card" style={{ textAlign: 'left', display: 'flex', gap: '2rem', alignItems: 'center' }}>
        <div style={{ minWidth: '200px' }}>
          <h3>Upload Resume</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Process via AI Engine</p>
        </div>
        <form onSubmit={handleUpload} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', flex: 1 }}>
          <textarea 
            placeholder="Paste Job Description here (Required for targeted matching)"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            style={{ width: '100%', minHeight: '80px', padding: '1rem', borderRadius: 'var(--radius-sm)', resize: 'vertical' }}
            required
          />
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <input 
              type="text" 
              placeholder="Candidate Name" 
              value={candidateName}
              onChange={(e) => setCandidateName(e.target.value)}
              style={{ flex: 1, padding: '0.875rem' }}
              required
            />
            <input 
              type="file" 
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files[0])}
              style={{ padding: '0.5rem', color: 'var(--text-muted)' }}
              required
            />
            <button type="submit" className="btn btn-primary" disabled={uploading}>
              {uploading ? 'Processing...' : 'Upload & Score'}
            </button>
          </div>
        </form>
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        <input 
          type="text" 
          placeholder="Search by name or skills (e.g., Python)..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ flex: 1, padding: '0.875rem' }}
        />
        <select 
          value={minScore}
          onChange={(e) => setMinScore(e.target.value)}
          style={{ padding: '0.875rem', minWidth: '150px' }}
        >
          <option value="0">All Scores</option>
          <option value="50">Score &gt; 50</option>
          <option value="70">Score &gt; 70</option>
          <option value="90">Score &gt; 90</option>
        </select>
        <button className="btn btn-primary" onClick={handleCluster} disabled={clustering}>
          {clustering ? 'Analyzing...' : 'Run AI Clustering'}
        </button>
        <button className="btn btn-glass" onClick={exportToCSV}>
          Export CSV
        </button>
      </div>

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
            {candidates.map(c => (
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
            {candidates.length === 0 && (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>No candidates found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default CandidateList;
