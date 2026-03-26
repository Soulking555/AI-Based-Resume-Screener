import React from 'react';

function CandidateProfile({ candidate }) {
  return (
    <div>
      <div className="header">
        <h1>{candidate.name}'s AI Report</h1>
        <p style={{ color: 'var(--text-muted)' }}>Explainable AI Scoring Breakdown</p>
      </div>

      <div className="profile-grid">
        {/* Left Column: XAI Breakdown */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          <div className="profile-card">
            <h3 style={{ marginBottom: '1.5rem', borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>
              Final Evaluation
            </h3>
            <div className="score-circle" style={{ borderColor: candidate.score >= 70 ? 'var(--success)' : candidate.score < 40 ? 'var(--danger)' : 'var(--warning)' }}>
              {candidate.score}%
            </div>
            
            <div className="recommendation-box">
              <strong>AI Recommendation:</strong><br/>
              {candidate.recommendation}
            </div>
          </div>

          <div className="profile-card">
            <h3 style={{ marginBottom: '1.5rem', borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>
              Explainable Scoring Breakdown
            </h3>
            
            <div style={{ marginBottom: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                <span>Skill Match (40% weight)</span>
                <span>{candidate.skills.length * 10}%</span>
              </div>
              <div className="progress-bar-container">
                <div className="progress-bar" style={{ width: `${Math.min(100, candidate.skills.length * 10)}%` }}></div>
              </div>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                <span>Experience (20% weight)</span>
                <span>{candidate.experience * 100}%</span>
              </div>
              <div className="progress-bar-container">
                <div className="progress-bar" style={{ width: `${candidate.experience * 100}%` }}></div>
              </div>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                <span>Education (10% weight)</span>
                <span>{candidate.education * 100}%</span>
              </div>
              <div className="progress-bar-container">
                <div className="progress-bar" style={{ width: `${candidate.education * 100}%` }}></div>
              </div>
            </div>
            
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '1rem' }}>
              Note: Similarity and Projects scores are aggregated into Final Score by matching engine.
            </p>
          </div>
          
        </div>

        {/* Right Column: Skills, Gaps, Interview Gen */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          <div className="profile-card">
            <h3 style={{ marginBottom: '1rem' }}>Detected Skills</h3>
            {candidate.skills.length > 0 ? candidate.skills.map(s => (
              <span key={s} className="skill-tag">{s}</span>
            )) : <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>No defined skills detected.</p>}
          </div>

          <div className="profile-card">
            <h3 style={{ marginBottom: '1rem' }}>Skill Gaps</h3>
            {candidate.missing_skills.length > 0 ? candidate.missing_skills.map(s => (
              <span key={s} className="skill-tag skill-missing">{s}</span>
            )) : <p style={{ color: 'var(--success)', fontSize: '0.875rem' }}>No major skill gaps detected!</p>}
          </div>

          <div className="profile-card">
            <h3 style={{ marginBottom: '1rem' }}>AI Interview Questions</h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
              Generated based on missing skills to test candidate adaptability.
            </p>
            <ul className="question-list" style={{ paddingLeft: '1.25rem' }}>
              {candidate.interview_questions && candidate.interview_questions.length > 0 ? (
                candidate.interview_questions.map((q, i) => (
                  <li key={i}>{q}</li>
                ))
              ) : (
                <li style={{ color: 'var(--text-muted)' }}>No targeted questions needed.</li>
              )}
            </ul>
          </div>

        </div>
      </div>
    </div>
  );
}

export default CandidateProfile;
