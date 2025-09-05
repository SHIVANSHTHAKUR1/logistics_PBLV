import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import Trips from './pages/Trips'
import Drivers from './pages/Drivers'
import Analytics from './pages/Analytics'
import NotificationSystem from './components/NotificationSystem'

// Placeholder components for other pages
const VehiclesPage = () => (
  <div>
    <h2>Vehicle Management</h2>
    <p>Fleet management and tracking coming soon...</p>
  </div>
)

const ExpensesPage = () => (
  <div>
    <h2>Expense Management</h2>
    <p>AI-powered expense tracking and analysis coming soon...</p>
  </div>
)



const SettingsPage = () => (
  <div>
    <h2>Settings</h2>
    <p>System configuration coming soon...</p>
  </div>
)

function App() {
  console.log('App component rendering...');
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/trips" element={<Trips />} />
        <Route path="/drivers" element={<Drivers />} />
        <Route path="/vehicles" element={<VehiclesPage />} />
        <Route path="/expenses" element={<ExpensesPage />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
      <NotificationSystem />
    </Layout>
  )
}

export default App
