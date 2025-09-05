import React, { useState, useEffect, useMemo } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { createSelector } from '@reduxjs/toolkit';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  IconButton,
  Tooltip,
  Badge,
  Divider,
  Alert,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  LocalShipping as TruckIcon,
  Person as PersonIcon,
  AttachMoney as MoneyIcon,
  Speed as SpeedIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Schedule as ScheduleIcon,
  LocationOn as LocationIcon,
  Notifications as NotificationsIcon,
  Refresh as RefreshIcon,
  MoreVert as MoreVertIcon,
  Navigation as NavigationIcon,
  Analytics as AnalyticsIcon,
  Assignment as AssignmentIcon,
} from '@mui/icons-material';
import { fetchDashboardStats, fetchRecentActivities } from '../store/slices/dashboardSlice';
import { fetchTrips } from '../store/slices/tripsSlice';
import { fetchDrivers } from '../store/slices/driversSlice';

// Memoized selector to prevent unnecessary rerenders
const selectDashboardData = createSelector(
  [(state) => state.trips?.list, (state) => state.drivers?.list, (state) => state.analytics],
  (trips, drivers, analytics) => ({
    trips: trips || [],
    drivers: drivers || [],
    analytics: analytics || {},
  })
);

function Dashboard() {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(fetchDashboardStats());
    dispatch(fetchRecentActivities());
    dispatch(fetchTrips());
    dispatch(fetchDrivers());
  }, [dispatch]);
  
  const { trips, drivers, analytics } = useSelector(selectDashboardData);

  const [realTimeData, setRealTimeData] = useState({
    totalTrips: 1247,
    tripsChange: 12.5,
    activeDrivers: 89,
    driversChange: 5.2,
    revenue: 2456000,
    revenueChange: 8.3,
    efficiency: 94.2,
    efficiencyChange: 2.1,
    activeTripsCount: 45,
    onTimeDelivery: 92.3,
    fuelEfficiency: 12.8,
    customerSatisfaction: 4.6,
  });

  const [recentTrips, setRecentTrips] = useState([
    {
      id: 'T001',
      pickup: 'Mumbai',
      delivery: 'Delhi',
      driver: 'Rajesh Kumar',
      status: 'in_progress',
      progress: 65,
      eta: '6 hours',
      priority: 'high',
    },
    {
      id: 'T002',
      pickup: 'Chennai',
      delivery: 'Bangalore',
      driver: 'Suresh Patil',
      status: 'pending',
      progress: 0,
      eta: '8 hours',
      priority: 'medium',
    },
    {
      id: 'T003',
      pickup: 'Pune',
      delivery: 'Hyderabad',
      driver: 'Vikram Singh',
      status: 'completed',
      progress: 100,
      eta: 'Delivered',
      priority: 'low',
    },
  ]);

  const [alerts, setAlerts] = useState([
    {
      id: 1,
      type: 'warning',
      message: 'Heavy traffic on Mumbai-Delhi route (NH-48)',
      time: '5 min ago',
    },
    {
      id: 2,
      type: 'success',
      message: 'Trip T003 delivered successfully',
      time: '12 min ago',
    },
    {
      id: 3,
      type: 'info',
      message: 'Driver Rajesh Kumar requested fuel stop',
      time: '18 min ago',
    },
    {
      id: 4,
      type: 'error',
      message: 'Vehicle MH-12-AB-3456 needs maintenance',
      time: '25 min ago',
    },
  ]);

  const [topDrivers, setTopDrivers] = useState([
    { id: '1', name: 'Rajesh Kumar', trips: 156, rating: 4.8, status: 'active' },
    { id: '2', name: 'Vikram Singh', trips: 203, rating: 4.2, status: 'active' },
    { id: '3', name: 'Suresh Patil', trips: 89, rating: 4.6, status: 'busy' },
    { id: '4', name: 'Amit Sharma', trips: 134, rating: 4.5, status: 'active' },
  ]);

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate random updates to metrics
      setRealTimeData(prev => ({
        ...prev,
        activeTripsCount: Math.max(30, prev.activeTripsCount + Math.floor(Math.random() * 6) - 3),
        onTimeDelivery: Math.max(85, Math.min(100, prev.onTimeDelivery + (Math.random() - 0.5))),
      }));
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const MetricCard = ({ title, value, change, icon, color = 'primary', subtitle }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start">
          <Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4" fontWeight="bold" color={`${color}.main`}>
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                {subtitle}
              </Typography>
            )}
            {change !== undefined && (
              <Box display="flex" alignItems="center" mt={1}>
                {change >= 0 ? (
                  <TrendingUpIcon color="success" sx={{ fontSize: 16, mr: 0.5 }} />
                ) : (
                  <TrendingDownIcon color="error" sx={{ fontSize: 16, mr: 0.5 }} />
                )}
                <Typography
                  variant="body2"
                  color={change >= 0 ? 'success.main' : 'error.main'}
                >
                  {Math.abs(change)}% from last week
                </Typography>
              </Box>
            )}
          </Box>
          <Box
            sx={{
              p: 1.5,
              borderRadius: 2,
              bgcolor: `${color}.light`,
              color: `${color}.main`,
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  const getStatusColor = (status) => {
    switch (status) {
      case 'in_progress':
        return 'primary';
      case 'completed':
        return 'success';
      case 'pending':
        return 'warning';
      case 'cancelled':
        return 'error';
      default:
        return 'default';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'warning':
        return <WarningIcon />;
      case 'success':
        return <CheckCircleIcon />;
      case 'error':
        return <WarningIcon />;
      default:
        return <NotificationsIcon />;
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Real-time logistics overview and insights
          </Typography>
        </Box>
        <Box display="flex" gap={1}>
          <Tooltip title="Refresh Data">
            <IconButton color="primary">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
          <Button variant="outlined" startIcon={<AnalyticsIcon />}>
            View Analytics
          </Button>
        </Box>
      </Box>

      {/* Key Metrics */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Total Trips"
            value={realTimeData.totalTrips.toLocaleString()}
            change={realTimeData.tripsChange}
            icon={<TruckIcon />}
            color="primary"
            subtitle={`${realTimeData.activeTripsCount} active`}
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Active Drivers"
            value={realTimeData.activeDrivers}
            change={realTimeData.driversChange}
            icon={<PersonIcon />}
            color="success"
            subtitle="Available for trips"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Revenue"
            value={`₹${(realTimeData.revenue / 1000000).toFixed(1)}M`}
            change={realTimeData.revenueChange}
            icon={<MoneyIcon />}
            color="warning"
            subtitle="This month"
          />
        </Grid>
        <Grid item xs={12} sm={6} lg={3}>
          <MetricCard
            title="Efficiency"
            value={`${realTimeData.efficiency}%`}
            change={realTimeData.efficiencyChange}
            icon={<SpeedIcon />}
            color="info"
            subtitle="Route optimization"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Recent Trips */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Recent Trips</Typography>
                <Button size="small">View All</Button>
              </Box>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Trip ID</TableCell>
                      <TableCell>Route</TableCell>
                      <TableCell>Driver</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Progress</TableCell>
                      <TableCell>ETA</TableCell>
                      <TableCell>Priority</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {recentTrips.map((trip) => (
                      <TableRow key={trip.id} hover>
                        <TableCell>{trip.id}</TableCell>
                        <TableCell>
                          <Box display="flex" alignItems="center">
                            <LocationIcon sx={{ fontSize: 16, mr: 1, color: 'primary.main' }} />
                            {trip.pickup} → {trip.delivery}
                          </Box>
                        </TableCell>
                        <TableCell>{trip.driver}</TableCell>
                        <TableCell>
                          <Chip
                            label={trip.status.replace('_', ' ')}
                            color={getStatusColor(trip.status)}
                            size="small"
                            sx={{ textTransform: 'capitalize' }}
                          />
                        </TableCell>
                        <TableCell>
                          <Box display="flex" alignItems="center" gap={1}>
                            <LinearProgress
                              variant="determinate"
                              value={trip.progress}
                              sx={{ flexGrow: 1, height: 6, borderRadius: 3 }}
                            />
                            <Typography variant="body2">{trip.progress}%</Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Box display="flex" alignItems="center">
                            <ScheduleIcon sx={{ fontSize: 16, mr: 1 }} />
                            {trip.eta}
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={trip.priority}
                            color={getPriorityColor(trip.priority)}
                            size="small"
                            variant="outlined"
                            sx={{ textTransform: 'capitalize' }}
                          />
                        </TableCell>
                        <TableCell>
                          <Tooltip title="Track">
                            <IconButton size="small">
                              <NavigationIcon />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="More">
                            <IconButton size="small">
                              <MoreVertIcon />
                            </IconButton>
                          </Tooltip>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Alerts & Notifications */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Alerts & Notifications</Typography>
                <Badge badgeContent={alerts.length} color="error">
                  <NotificationsIcon />
                </Badge>
              </Box>
              <List sx={{ maxHeight: 300, overflow: 'auto' }}>
                {alerts.map((alert, index) => (
                  <React.Fragment key={alert.id}>
                    <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                      <ListItemAvatar>
                        <Avatar
                          sx={{
                            bgcolor:
                              alert.type === 'warning'
                                ? 'warning.main'
                                : alert.type === 'success'
                                ? 'success.main'
                                : alert.type === 'error'
                                ? 'error.main'
                                : 'info.main',
                            width: 32,
                            height: 32,
                          }}
                        >
                          {getAlertIcon(alert.type)}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={alert.message}
                        secondary={alert.time}
                        primaryTypographyProps={{ variant: 'body2' }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                    {index < alerts.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Performance Metrics */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Performance Metrics
              </Typography>
              <Box mt={2}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="body2">On-Time Delivery</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {realTimeData.onTimeDelivery.toFixed(1)}%
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={realTimeData.onTimeDelivery}
                  color="success"
                  sx={{ height: 8, borderRadius: 4, mb: 3 }}
                />

                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="body2">Fuel Efficiency</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {realTimeData.fuelEfficiency} km/l
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={(realTimeData.fuelEfficiency / 15) * 100}
                  color="primary"
                  sx={{ height: 8, borderRadius: 4, mb: 3 }}
                />

                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="body2">Customer Satisfaction</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {realTimeData.customerSatisfaction}/5
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={(realTimeData.customerSatisfaction / 5) * 100}
                  color="warning"
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Top Drivers */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Top Drivers</Typography>
                <Button size="small">View All</Button>
              </Box>
              <List sx={{ pt: 0 }}>
                {topDrivers.map((driver, index) => (
                  <ListItem key={driver.id} sx={{ px: 0 }}>
                    <ListItemAvatar>
                      <Badge
                        overlap="circular"
                        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                        badgeContent={
                          <Box
                            sx={{
                              width: 12,
                              height: 12,
                              borderRadius: '50%',
                              bgcolor: driver.status === 'active' ? 'success.main' : 'warning.main',
                              border: '2px solid white',
                            }}
                          />
                        }
                      >
                        <Avatar>
                          {driver.name.split(' ').map(n => n[0]).join('')}
                        </Avatar>
                      </Badge>
                    </ListItemAvatar>
                    <ListItemText
                      primary={driver.name}
                      secondary={
                        <Box component="span">
                          <Typography variant="body2" component="span">
                            {driver.trips} trips • ⭐ {driver.rating}
                          </Typography>
                        </Box>
                      }
                    />
                    <Chip
                      label={`#${index + 1}`}
                      color={index === 0 ? 'warning' : 'default'}
                      size="small"
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<TruckIcon />}
                    sx={{ py: 1.5 }}
                  >
                    Create New Trip
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<PersonIcon />}
                    sx={{ py: 1.5 }}
                  >
                    Add Driver
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<AssignmentIcon />}
                    sx={{ py: 1.5 }}
                  >
                    Assign Trip
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<AnalyticsIcon />}
                    sx={{ py: 1.5 }}
                  >
                    View Reports
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
