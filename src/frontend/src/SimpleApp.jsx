import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Box, Typography } from '@mui/material'

// Simple test components
const Dashboard = () => (
  <Box p={3}>
    <Typography variant="h4">Dashboard</Typography>
    <Typography>Welcome to the AI Logistics Management System</Typography>
  </Box>
)

const Trips = () => (
  <Box p={3}>
    <Typography variant="h4">Trips</Typography>
    <Typography>Trip management coming soon...</Typography>
  </Box>
)

function SimpleApp() {
  return (
    <Box>
      <Box sx={{ backgroundColor: 'primary.main', color: 'white', p: 2 }}>
        <Typography variant="h6">AI Logistics System</Typography>
      </Box>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/trips" element={<Trips />} />
      </Routes>
    </Box>
  )
}

export default SimpleApp
