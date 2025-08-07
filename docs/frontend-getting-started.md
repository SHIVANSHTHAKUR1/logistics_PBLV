# Getting Started Guide - Frontend Development (Shashank Kumar Pathania)

## 🎯 Your Role: Frontend Lead & Integration Specialist

You'll be responsible for building the React.js web dashboard, user interfaces, and integrating everything with the backend APIs.

---

## 🛠️ Development Environment Setup

### Step 1: Install Required Software
```bash
# Install Node.js 18+ from nodejs.org
# Verify installation
node --version
npm --version

# Install Git (if not already installed)
# Download from git-scm.com

# Install VS Code
# Download from code.visualstudio.com
```

### Step 2: Install VS Code Extensions
- ES7+ React/Redux/React-Native snippets
- Auto Rename Tag
- Bracket Pair Colorizer
- Thunder Client (for API testing)
- GitLens
- Prettier - Code formatter
- ESLint

### Step 3: Create React Application
```bash
# Navigate to your project folder
cd "c:\Users\shiva\OneDrive\Desktop\College\New folder\src"

# Create React app
npx create-react-app frontend
cd frontend

# Install additional packages
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/icons-material
npm install react-router-dom
npm install axios
npm install @reduxjs/toolkit react-redux
npm install recharts  # For charts and analytics
npm install @mui/x-data-grid  # For data tables
```

---

## 📁 Your Folder Structure

Organize your React app like this:
```
src/frontend/
├── public/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── common/          # Common components (buttons, inputs, etc.)
│   │   ├── layout/          # Layout components (navbar, sidebar)
│   │   └── forms/           # Form components
│   ├── pages/               # Page components
│   │   ├── Dashboard/
│   │   ├── Drivers/
│   │   ├── Trips/
│   │   ├── Finance/
│   │   └── Auth/
│   ├── store/               # Redux store
│   ├── services/            # API service calls
│   ├── utils/               # Utility functions
│   ├── hooks/               # Custom React hooks
│   └── styles/              # Global styles and themes
```

---

## 🎨 Week 1 Tasks - Project Setup & Design System

### Task 1: Setup Material-UI Theme
Create `src/styles/theme.js`:
```javascript
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Blue for primary actions
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#ff9800', // Orange for secondary actions
      light: '#ffb74d',
      dark: '#f57c00',
    },
    success: {
      main: '#4caf50', // Green for success states
    },
    warning: {
      main: '#ff9800', // Orange for warnings
    },
    error: {
      main: '#f44336', // Red for errors
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: [
      'Roboto',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontWeight: 500,
      fontSize: '2.5rem',
    },
    h2: {
      fontWeight: 500,
      fontSize: '2rem',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none', // Remove uppercase transformation
          borderRadius: 8,
        },
      },
    },
  },
});

export default theme;
```

### Task 2: Setup Routing
Create `src/App.js`:
```javascript
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Provider } from 'react-redux';

import theme from './styles/theme';
import store from './store/store';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import Drivers from './pages/Drivers/Drivers';
import Trips from './pages/Trips/Trips';
import Finance from './pages/Finance/Finance';
import Login from './pages/Auth/Login';

function App() {
  const isAuthenticated = false; // Replace with actual auth check

  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/"
              element={
                isAuthenticated ? (
                  <Layout>
                    <Dashboard />
                  </Layout>
                ) : (
                  <Navigate to="/login" />
                )
              }
            />
            <Route
              path="/drivers"
              element={
                <Layout>
                  <Drivers />
                </Layout>
              }
            />
            <Route
              path="/trips"
              element={
                <Layout>
                  <Trips />
                </Layout>
              }
            />
            <Route
              path="/finance"
              element={
                <Layout>
                  <Finance />
                </Layout>
              }
            />
          </Routes>
        </Router>
      </ThemeProvider>
    </Provider>
  );
}

export default App;
```

### Task 3: Create Layout Component
Create `src/components/layout/Layout.js`:
```javascript
import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Box,
  IconButton,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  LocalShipping as TruckIcon,
  AttachMoney as MoneyIcon,
} from '@mui/icons-material';
import { Link, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Drivers', icon: <PeopleIcon />, path: '/drivers' },
  { text: 'Trips', icon: <TruckIcon />, path: '/trips' },
  { text: 'Finance', icon: <MoneyIcon />, path: '/finance' },
];

function Layout({ children }) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap>
          Logistics Manager
        </Typography>
      </Toolbar>
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            component={Link}
            to={item.path}
            selected={location.pathname === item.path}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${drawerWidth}px)` },
          ml: { md: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Logistics Management System
          </Typography>
        </Toolbar>
      </AppBar>

      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}

export default Layout;
```

---

## 🔐 Week 2 Tasks - Authentication & State Management

### Task 1: Redux Store Setup
Create `src/store/store.js`:
```javascript
import { configureStore } from '@reduxjs/toolkit';
import authSlice from './slices/authSlice';
import driversSlice from './slices/driversSlice';
import tripsSlice from './slices/tripsSlice';

const store = configureStore({
  reducer: {
    auth: authSlice,
    drivers: driversSlice,
    trips: tripsSlice,
  },
});

export default store;
```

### Task 2: Authentication Slice
Create `src/store/slices/authSlice.js`:
```javascript
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import authService from '../../services/authService';

// Async thunks
export const loginUser = createAsyncThunk(
  'auth/login',
  async ({ username, password }, { rejectWithValue }) => {
    try {
      const response = await authService.login(username, password);
      localStorage.setItem('token', response.data.token);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data.message);
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    token: localStorage.getItem('token'),
    isLoading: false,
    error: null,
  },
  reducers: {
    logout: (state) => {
      localStorage.removeItem('token');
      state.user = null;
      state.token = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const { logout, clearError } = authSlice.actions;
export default authSlice.reducer;
```

### Task 3: API Service Setup
Create `src/services/api.js`:
```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle authentication errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

## 📊 Week 3-4 Tasks - Core Dashboard Features

### Task 1: Dashboard Overview
Create `src/pages/Dashboard/Dashboard.js`:
```javascript
import React, { useEffect, useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
} from '@mui/material';
import {
  TrendingUp,
  LocalShipping,
  People,
  AttachMoney,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function Dashboard() {
  const [stats, setStats] = useState({
    totalTrips: 0,
    activeDrivers: 0,
    todayRevenue: 0,
    monthlyProfit: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch dashboard data
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    // Implementation to fetch data from backend
    setLoading(false);
  };

  const StatCard = ({ title, value, icon, color }) => (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="div">
              {value}
            </Typography>
          </Box>
          <Box sx={{ color }}>
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Active Trips"
            value={stats.totalTrips}
            icon={<LocalShipping fontSize="large" />}
            color="primary.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Available Drivers"
            value={stats.activeDrivers}
            icon={<People fontSize="large" />}
            color="success.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Today's Revenue"
            value={`₹${stats.todayRevenue.toLocaleString()}`}
            icon={<AttachMoney fontSize="large" />}
            color="warning.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Monthly Profit"
            value={`₹${stats.monthlyProfit.toLocaleString()}`}
            icon={<TrendingUp fontSize="large" />}
            color="error.main"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Revenue Trend
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={[]}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="revenue" stroke="#8884d8" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activities
              </Typography>
              {/* Add activity list here */}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
```

### Task 2: Driver Management Page
Create `src/pages/Drivers/Drivers.js`:
```javascript
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  Avatar,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import {
  Add as AddIcon,
  Phone as PhoneIcon,
  Edit as EditIcon,
  CheckCircle,
  Cancel,
} from '@mui/icons-material';

function Drivers() {
  const [drivers, setDrivers] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedDriver, setSelectedDriver] = useState(null);

  useEffect(() => {
    fetchDrivers();
  }, []);

  const fetchDrivers = async () => {
    // Implementation to fetch drivers from backend
  };

  const DriverCard = ({ driver }) => (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Avatar sx={{ mr: 2 }}>{driver.name.charAt(0)}</Avatar>
          <Box flexGrow={1}>
            <Typography variant="h6">{driver.name}</Typography>
            <Typography color="textSecondary">{driver.phone}</Typography>
          </Box>
          <Chip
            label={driver.isAvailable ? 'Available' : 'Busy'}
            color={driver.isAvailable ? 'success' : 'default'}
            icon={driver.isAvailable ? <CheckCircle /> : <Cancel />}
          />
        </Box>
        
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="body2" color="textSecondary">
            License: {driver.licenseNumber}
          </Typography>
          <Box>
            <IconButton color="primary">
              <PhoneIcon />
            </IconButton>
            <IconButton color="primary">
              <EditIcon />
            </IconButton>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Drivers</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          Add Driver
        </Button>
      </Box>

      <Grid container spacing={3}>
        {drivers.map((driver) => (
          <Grid item xs={12} sm={6} md={4} key={driver.id}>
            <DriverCard driver={driver} />
          </Grid>
        ))}
      </Grid>

      {/* Add Driver Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add New Driver</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField fullWidth label="Driver Name" variant="outlined" />
            </Grid>
            <Grid item xs={12}>
              <TextField fullWidth label="Phone Number" variant="outlined" />
            </Grid>
            <Grid item xs={12}>
              <TextField fullWidth label="License Number" variant="outlined" />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button variant="contained">Add Driver</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Drivers;
```

---

## 📱 Week 5-6 Tasks - Advanced Features & Mobile Optimization

### Task 1: Trip Management Interface
Create comprehensive trip creation, tracking, and management interfaces.

### Task 2: Real-time Updates
Implement WebSocket connections for real-time updates:
```javascript
// src/hooks/useWebSocket.js
import { useEffect, useRef } from 'react';

const useWebSocket = (url, onMessage) => {
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(url);
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    return () => {
      ws.current.close();
    };
  }, [url, onMessage]);

  const sendMessage = (message) => {
    if (ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  };

  return sendMessage;
};

export default useWebSocket;
```

### Task 3: Mobile Responsive Design
Ensure all components work well on mobile devices using Material-UI's responsive features.

---

## 🧪 Testing Your Work

### Component Testing
Create `src/components/__tests__/Dashboard.test.js`:
```javascript
import React from 'react';
import { render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import { ThemeProvider } from '@mui/material/styles';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from '../pages/Dashboard/Dashboard';
import store from '../store/store';
import theme from '../styles/theme';

const renderWithProviders = (component) => {
  return render(
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <BrowserRouter>
          {component}
        </BrowserRouter>
      </ThemeProvider>
    </Provider>
  );
};

test('renders dashboard title', () => {
  renderWithProviders(<Dashboard />);
  const titleElement = screen.getByText(/Dashboard/i);
  expect(titleElement).toBeInTheDocument();
});
```

---

## 📊 Weekly Deliverables

**Week 1:**
- [ ] React app setup with Material-UI
- [ ] Routing configured
- [ ] Basic layout with navigation
- [ ] Theme and styling system

**Week 2:**
- [ ] Authentication pages (login/register)
- [ ] Redux store setup
- [ ] API integration layer
- [ ] Protected routes implemented

**Week 3:**
- [ ] Dashboard with stats cards
- [ ] Driver management interface
- [ ] Basic CRUD operations UI

**Week 4:**
- [ ] Trip management interface
- [ ] Real-time updates working
- [ ] Mobile responsive design
- [ ] Integration with backend APIs

Remember: Focus on user experience and make the interface intuitive for truck owners who may not be tech-savvy!
