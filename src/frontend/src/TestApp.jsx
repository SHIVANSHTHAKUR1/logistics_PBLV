import React from 'react'

function TestApp() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Test App</h1>
      <p>If you can see this, React is working!</p>
      <div style={{ background: '#f0f0f0', padding: '10px', margin: '10px 0' }}>
        <h2>Debug Info:</h2>
        <p>React version: {React.version}</p>
        <p>Environment: {import.meta.env.MODE}</p>
        <p>Timestamp: {new Date().toISOString()}</p>
      </div>
    </div>
  )
}

export default TestApp
