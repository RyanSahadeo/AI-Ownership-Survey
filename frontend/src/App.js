import React, { useEffect } from 'react';

function App() {
  useEffect(() => {
    // Redirect to the Streamlit backend
    window.location.href = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
  }, []);

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      backgroundColor: '#f8f9fa',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{ textAlign: 'center' }}>
        <h2>Redirecting to POQ Survey Platform...</h2>
        <p>Please wait while you are redirected to the survey application.</p>
        <p>If not redirected automatically, <a href={process.env.REACT_APP_BACKEND_URL}>click here</a>.</p>
      </div>
    </div>
  );
}

export default App;
