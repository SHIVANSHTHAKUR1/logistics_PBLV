import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Tab,
  Tabs,
  MenuItem,
  TextField,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  Chip,
  Tooltip,
  IconButton,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  LocalShipping as TruckIcon,
  Person as PersonIcon,
  AttachMoney as MoneyIcon,
  Assessment as AssessmentIcon,
  Timeline as TimelineIcon,
  PieChart as PieChartIcon,
  BarChart as BarChartIcon,
  ShowChart as ShowChartIcon,
  Download as DownloadIcon,
  Refresh as RefreshIcon,
  DateRange as DateRangeIcon,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';

// Mock chart component - in real app, use recharts, chart.js, or similar
const MockChart = ({ type, data, height = 300 }) => (
  <Box
    sx={{
      height,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      bgcolor: 'grey.50',
      borderRadius: 1,
      border: '1px solid',
      borderColor: 'grey.200',
    }}
  >
    <Box textAlign="center">
      {type === 'line' && <ShowChartIcon sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />}
      {type === 'bar' && <BarChartIcon sx={{ fontSize: 48, color: 'secondary.main', mb: 1 }} />}
      {type === 'pie' && <PieChartIcon sx={{ fontSize: 48, color: 'success.main', mb: 1 }} />}
      <Typography variant="body2" color="text.secondary">
        {type.toUpperCase()} Chart - {data}
      </Typography>
      <Typography variant="caption" color="text.secondary">
        Interactive chart would render here
      </Typography>
    </Box>
  </Box>
);

function Analytics() {
  const dispatch = useDispatch();
  const { analytics, loading } = useSelector((state) => ({
    analytics: state.analytics || {},
    loading: state.analytics?.loading || false,
  }));

  const [tabValue, setTabValue] = useState(0);
  const [dateRange, setDateRange] = useState('7d');
  const [selectedMetric, setSelectedMetric] = useState('trips');

  // Mock analytics data
  const mockAnalytics = {
    overview: {
      totalTrips: 1247,
      tripsChange: 12.5,
      totalRevenue: 2456000,
      revenueChange: 8.3,
      activeDrivers: 156,
      driversChange: -2.1,
      avgDeliveryTime: 18.5,
      deliveryTimeChange: -5.2,
      fuelEfficiency: 12.8,
      fuelEfficiencyChange: 3.1,
      customerSatisfaction: 4.6,
      satisfactionChange: 0.3,
    },
    tripAnalytics: {
      completed: 1156,
      inProgress: 45,
      pending: 32,
      cancelled: 14,
      onTimeDelivery: 92.3,
      averageDistance: 245,
      totalDistance: 283420,
    },
    driverPerformance: {
      topDrivers: [
        { id: '1', name: 'Rajesh Kumar', trips: 156, rating: 4.8, onTime: 95 },
        { id: '2', name: 'Vikram Singh', trips: 203, rating: 4.2, onTime: 92 },
        { id: '3', name: 'Suresh Patil', trips: 89, rating: 4.6, onTime: 88 },
        { id: '4', name: 'Amit Sharma', trips: 134, rating: 4.5, onTime: 91 },
        { id: '5', name: 'Ravi Gupta', trips: 167, rating: 4.7, onTime: 94 },
      ],
      averageRating: 4.56,
      driverUtilization: 78.5,
    },
    financialMetrics: {
      monthlyRevenue: [
        { month: 'Jan', revenue: 2100000, profit: 315000 },
        { month: 'Feb', revenue: 2350000, profit: 352500 },
        { month: 'Mar', revenue: 2456000, profit: 368400 },
      ],
      costBreakdown: {
        fuel: 45,
        maintenance: 15,
        driver_wages: 25,
        insurance: 8,
        other: 7,
      },
      profitMargin: 15.2,
      operatingExpenses: 2078400,
    },
    routeOptimization: {
      avgFuelSavings: 18.5,
      avgTimeSavings: 22.3,
      co2Reduction: 1250,
      optimizedRoutes: 892,
      totalRoutes: 1156,
    },
    realTimeMetrics: {
      activeTrips: 45,
      availableDrivers: 89,
      busyDrivers: 67,
      averageSpeed: 52.5,
      trafficAlerts: 12,
      weatherAlerts: 3,
    },
  };

  useEffect(() => {
    // In a real app, dispatch action to fetch analytics
    // dispatch(fetchAnalytics({ dateRange }));
  }, [dispatch, dateRange]);

  const MetricCard = ({ title, value, change, icon, color = 'primary' }) => (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start">
          <Box>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h5" fontWeight="bold">
              {value}
            </Typography>
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
                  {Math.abs(change)}%
                </Typography>
              </Box>
            )}
          </Box>
          <Box
            sx={{
              p: 1,
              borderRadius: 1,
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

  const OverviewTab = () => (
    <Grid container spacing={3}>
      {/* Key Metrics */}
      <Grid item xs={12} md={6} lg={3}>
        <MetricCard
          title="Total Trips"
          value={mockAnalytics.overview.totalTrips.toLocaleString()}
          change={mockAnalytics.overview.tripsChange}
          icon={<TruckIcon />}
          color="primary"
        />
      </Grid>
      <Grid item xs={12} md={6} lg={3}>
        <MetricCard
          title="Total Revenue"
          value={`₹${(mockAnalytics.overview.totalRevenue / 1000000).toFixed(1)}M`}
          change={mockAnalytics.overview.revenueChange}
          icon={<MoneyIcon />}
          color="success"
        />
      </Grid>
      <Grid item xs={12} md={6} lg={3}>
        <MetricCard
          title="Active Drivers"
          value={mockAnalytics.overview.activeDrivers}
          change={mockAnalytics.overview.driversChange}
          icon={<PersonIcon />}
          color="info"
        />
      </Grid>
      <Grid item xs={12} md={6} lg={3}>
        <MetricCard
          title="Avg Delivery Time"
          value={`${mockAnalytics.overview.avgDeliveryTime}h`}
          change={mockAnalytics.overview.deliveryTimeChange}
          icon={<TimelineIcon />}
          color="warning"
        />
      </Grid>

      {/* Charts */}
      <Grid item xs={12} lg={8}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Trip Trends
            </Typography>
            <MockChart type="line" data="Daily Trips vs Revenue" height={300} />
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} lg={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Trip Status Distribution
            </Typography>
            <MockChart type="pie" data="Completed, In Progress, Pending" height={300} />
          </CardContent>
        </Card>
      </Grid>

      {/* Additional Metrics */}
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Fuel Efficiency
            </Typography>
            <Typography variant="h4" color="success.main">
              {mockAnalytics.overview.fuelEfficiency} km/l
            </Typography>
            <Box display="flex" alignItems="center" mt={1}>
              <TrendingUpIcon color="success" sx={{ fontSize: 16, mr: 0.5 }} />
              <Typography variant="body2" color="success.main">
                {mockAnalytics.overview.fuelEfficiencyChange}% improvement
              </Typography>
            </Box>
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Customer Satisfaction
            </Typography>
            <Typography variant="h4" color="primary.main">
              {mockAnalytics.overview.customerSatisfaction}/5
            </Typography>
            <LinearProgress
              variant="determinate"
              value={(mockAnalytics.overview.customerSatisfaction / 5) * 100}
              sx={{ mt: 2, height: 8, borderRadius: 4 }}
            />
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              On-Time Delivery
            </Typography>
            <Typography variant="h4" color="success.main">
              {mockAnalytics.tripAnalytics.onTimeDelivery}%
            </Typography>
            <LinearProgress
              variant="determinate"
              value={mockAnalytics.tripAnalytics.onTimeDelivery}
              color="success"
              sx={{ mt: 2, height: 8, borderRadius: 4 }}
            />
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  const TripsTab = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} lg={8}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Trip Volume Analysis
            </Typography>
            <MockChart type="bar" data="Daily Trip Volumes" height={350} />
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} lg={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Trip Statistics
            </Typography>
            <Box mt={2}>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Completed</Typography>
                <Typography variant="body2" fontWeight="bold">
                  {mockAnalytics.tripAnalytics.completed}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">In Progress</Typography>
                <Typography variant="body2" fontWeight="bold" color="warning.main">
                  {mockAnalytics.tripAnalytics.inProgress}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Pending</Typography>
                <Typography variant="body2" fontWeight="bold" color="info.main">
                  {mockAnalytics.tripAnalytics.pending}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Cancelled</Typography>
                <Typography variant="body2" fontWeight="bold" color="error.main">
                  {mockAnalytics.tripAnalytics.cancelled}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Average Distance</Typography>
                <Typography variant="body2" fontWeight="bold">
                  {mockAnalytics.tripAnalytics.averageDistance} km
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between">
                <Typography variant="body2">Total Distance</Typography>
                <Typography variant="body2" fontWeight="bold">
                  {mockAnalytics.tripAnalytics.totalDistance.toLocaleString()} km
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Route Performance
            </Typography>
            <MockChart type="line" data="Route Efficiency vs Time" height={300} />
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  const DriversTab = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} lg={8}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Top Performing Drivers
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Rank</TableCell>
                    <TableCell>Driver Name</TableCell>
                    <TableCell>Trips</TableCell>
                    <TableCell>Rating</TableCell>
                    <TableCell>On-Time %</TableCell>
                    <TableCell>Performance</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockAnalytics.driverPerformance.topDrivers.map((driver, index) => (
                    <TableRow key={driver.id}>
                      <TableCell>
                        <Chip
                          label={index + 1}
                          color={index === 0 ? 'warning' : index === 1 ? 'default' : 'primary'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{driver.name}</TableCell>
                      <TableCell>{driver.trips}</TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          <Typography variant="body2">{driver.rating}</Typography>
                          <TrendingUpIcon 
                            color="success" 
                            sx={{ fontSize: 16, ml: 0.5 }} 
                          />
                        </Box>
                      </TableCell>
                      <TableCell>{driver.onTime}%</TableCell>
                      <TableCell>
                        <LinearProgress
                          variant="determinate"
                          value={driver.onTime}
                          color={driver.onTime > 90 ? 'success' : 'warning'}
                          sx={{ width: 80, height: 6, borderRadius: 3 }}
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} lg={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Driver Metrics
            </Typography>
            <Box mt={2}>
              <Typography variant="body2" gutterBottom>
                Average Rating
              </Typography>
              <Typography variant="h4" color="primary.main" gutterBottom>
                {mockAnalytics.driverPerformance.averageRating}/5
              </Typography>
              
              <Typography variant="body2" gutterBottom sx={{ mt: 3 }}>
                Driver Utilization
              </Typography>
              <Typography variant="h4" color="success.main" gutterBottom>
                {mockAnalytics.driverPerformance.driverUtilization}%
              </Typography>
              
              <LinearProgress
                variant="determinate"
                value={mockAnalytics.driverPerformance.driverUtilization}
                color="success"
                sx={{ mt: 1, height: 8, borderRadius: 4 }}
              />
            </Box>
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Driver Performance Trends
            </Typography>
            <MockChart type="line" data="Driver Performance Over Time" height={300} />
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  const FinancialsTab = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} lg={8}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Revenue & Profit Trends
            </Typography>
            <MockChart type="line" data="Monthly Revenue and Profit" height={350} />
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} lg={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Cost Breakdown
            </Typography>
            <MockChart type="pie" data="Operational Costs" height={350} />
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} md={4}>
        <MetricCard
          title="Profit Margin"
          value={`${mockAnalytics.financialMetrics.profitMargin}%`}
          change={2.1}
          icon={<AssessmentIcon />}
          color="success"
        />
      </Grid>
      
      <Grid item xs={12} md={4}>
        <MetricCard
          title="Operating Expenses"
          value={`₹${(mockAnalytics.financialMetrics.operatingExpenses / 1000000).toFixed(1)}M`}
          change={-3.2}
          icon={<MoneyIcon />}
          color="warning"
        />
      </Grid>
      
      <Grid item xs={12} md={4}>
        <MetricCard
          title="ROI"
          value="18.5%"
          change={4.2}
          icon={<TrendingUpIcon />}
          color="primary"
        />
      </Grid>
    </Grid>
  );

  const AIInsightsTab = () => (
    <Grid container spacing={3}>
      <Grid item xs={12} lg={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Route Optimization Impact
            </Typography>
            <Box mt={2}>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Fuel Savings</Typography>
                <Typography variant="body2" fontWeight="bold" color="success.main">
                  {mockAnalytics.routeOptimization.avgFuelSavings}%
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Time Savings</Typography>
                <Typography variant="body2" fontWeight="bold" color="success.main">
                  {mockAnalytics.routeOptimization.avgTimeSavings}%
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">CO2 Reduction</Typography>
                <Typography variant="body2" fontWeight="bold" color="success.main">
                  {mockAnalytics.routeOptimization.co2Reduction} kg
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Optimized Routes</Typography>
                <Typography variant="body2" fontWeight="bold">
                  {mockAnalytics.routeOptimization.optimizedRoutes} / {mockAnalytics.routeOptimization.totalRoutes}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} lg={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Real-time Metrics
            </Typography>
            <Box mt={2}>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Active Trips</Typography>
                <Typography variant="body2" fontWeight="bold" color="primary.main">
                  {mockAnalytics.realTimeMetrics.activeTrips}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Available Drivers</Typography>
                <Typography variant="body2" fontWeight="bold" color="success.main">
                  {mockAnalytics.realTimeMetrics.availableDrivers}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Average Speed</Typography>
                <Typography variant="body2" fontWeight="bold">
                  {mockAnalytics.realTimeMetrics.averageSpeed} km/h
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mb={2}>
                <Typography variant="body2">Traffic Alerts</Typography>
                <Typography variant="body2" fontWeight="bold" color="warning.main">
                  {mockAnalytics.realTimeMetrics.trafficAlerts}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              AI Predictions & Recommendations
            </Typography>
            <MockChart type="line" data="Demand Forecasting" height={300} />
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Analytics Dashboard</Typography>
        <Box display="flex" gap={2}>
          <TextField
            select
            size="small"
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            sx={{ minWidth: 120 }}
          >
            <MenuItem value="1d">Last 24h</MenuItem>
            <MenuItem value="7d">Last 7 days</MenuItem>
            <MenuItem value="30d">Last 30 days</MenuItem>
            <MenuItem value="90d">Last 3 months</MenuItem>
            <MenuItem value="1y">Last year</MenuItem>
          </TextField>
          <Tooltip title="Refresh Data">
            <IconButton color="primary">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
          >
            Export Report
          </Button>
        </Box>
      </Box>

      <Paper sx={{ width: '100%', mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={(event, newValue) => setTabValue(newValue)}
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab label="Overview" />
          <Tab label="Trip Analytics" />
          <Tab label="Driver Performance" />
          <Tab label="Financial Metrics" />
          <Tab label="AI Insights" />
        </Tabs>
      </Paper>

      <Box sx={{ mt: 3 }}>
        {tabValue === 0 && <OverviewTab />}
        {tabValue === 1 && <TripsTab />}
        {tabValue === 2 && <DriversTab />}
        {tabValue === 3 && <FinancialsTab />}
        {tabValue === 4 && <AIInsightsTab />}
      </Box>
    </Box>
  );
}

export default Analytics;
