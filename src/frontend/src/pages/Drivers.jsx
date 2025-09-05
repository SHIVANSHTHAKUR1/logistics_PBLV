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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Tooltip,
  Badge,
  LinearProgress,
  Tab,
  Tabs,
  Rating,
} from '@mui/material';
import {
  Add as AddIcon,
  Person as PersonIcon,
  Phone as PhoneIcon,
  LocationOn as LocationIcon,
  DirectionsCar as CarIcon,
  Star as StarIcon,
  Assignment as AssignmentIcon,
  Schedule as ScheduleIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Block as BlockIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Message as MessageIcon,
  Call as CallIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDrivers } from '../store/slices/driversSlice';

const driverStatuses = [
  { value: 'available', label: 'Available', color: 'success' },
  { value: 'busy', label: 'Busy', color: 'warning' },
  { value: 'on_trip', label: 'On Trip', color: 'primary' },
  { value: 'offline', label: 'Offline', color: 'default' },
  { value: 'suspended', label: 'Suspended', color: 'error' },
];

const licenseTypes = [
  'Light Motor Vehicle (LMV)',
  'Heavy Motor Vehicle (HMV)',
  'Transport Vehicle',
  'Hazardous Materials',
  'Public Service Vehicle',
];

function Drivers() {
  const dispatch = useDispatch();
  const { drivers, loading } = useSelector((state) => ({
    drivers: state.drivers.list || [],
    loading: state.drivers.loading || false,
  }));

  const [openDialog, setOpenDialog] = useState(false);
  const [selectedDriver, setSelectedDriver] = useState(null);
  const [dialogMode, setDialogMode] = useState('create'); // 'create', 'edit', 'view'
  const [filterStatus, setFilterStatus] = useState('all');
  const [tabValue, setTabValue] = useState(0);
  const [driverForm, setDriverForm] = useState({
    name: '',
    phone: '',
    email: '',
    license_number: '',
    license_type: '',
    license_expiry: '',
    address: '',
    emergency_contact: '',
    vehicle_assigned: '',
    status: 'available',
  });

  useEffect(() => {
    dispatch(fetchDrivers());
  }, [dispatch]);

  

  // Mock data for demonstration
  const mockDrivers = [
    {
      id: '1',
      name: 'Rajesh Kumar',
      phone: '+91-9876543210',
      email: 'rajesh.kumar@example.com',
      license_number: 'DL1420110012345',
      license_type: 'Heavy Motor Vehicle (HMV)',
      license_expiry: '2025-03-15',
      address: 'Mumbai, Maharashtra',
      emergency_contact: '+91-9876543211',
      vehicle_assigned: 'MH-01-AB-1234',
      status: 'on_trip',
      rating: 4.8,
      trips_completed: 156,
      total_distance: 45000,
      earnings_this_month: 45000,
      experience_years: 8,
      last_active: '2024-01-15T10:30:00',
      current_location: 'Highway NH-48, Gujarat',
      profile_image: null,
      documents: {
        license: 'verified',
        aadhar: 'verified',
        pan: 'verified',
        medical: 'pending',
      },
      performance: {
        on_time_delivery: 95,
        fuel_efficiency: 12.5,
        customer_rating: 4.8,
        safety_score: 92,
      },
    },
    {
      id: '2',
      name: 'Suresh Patil',
      phone: '+91-9876543220',
      email: 'suresh.patil@example.com',
      license_number: 'DL1420110012346',
      license_type: 'Transport Vehicle',
      license_expiry: '2024-12-20',
      address: 'Pune, Maharashtra',
      emergency_contact: '+91-9876543221',
      vehicle_assigned: 'MH-12-CD-5678',
      status: 'available',
      rating: 4.6,
      trips_completed: 89,
      total_distance: 28000,
      earnings_this_month: 32000,
      experience_years: 5,
      last_active: '2024-01-15T11:00:00',
      current_location: 'Pune Depot',
      profile_image: null,
      documents: {
        license: 'verified',
        aadhar: 'verified',
        pan: 'pending',
        medical: 'verified',
      },
      performance: {
        on_time_delivery: 88,
        fuel_efficiency: 11.8,
        customer_rating: 4.6,
        safety_score: 85,
      },
    },
    {
      id: '3',
      name: 'Vikram Singh',
      phone: '+91-9876543230',
      email: 'vikram.singh@example.com',
      license_number: 'DL1420110012347',
      license_type: 'Heavy Motor Vehicle (HMV)',
      license_expiry: '2025-08-10',
      address: 'Delhi, India',
      emergency_contact: '+91-9876543231',
      vehicle_assigned: null,
      status: 'offline',
      rating: 4.2,
      trips_completed: 203,
      total_distance: 67000,
      earnings_this_month: 28000,
      experience_years: 12,
      last_active: '2024-01-14T18:30:00',
      current_location: 'Delhi Depot',
      profile_image: null,
      documents: {
        license: 'verified',
        aadhar: 'verified',
        pan: 'verified',
        medical: 'expired',
      },
      performance: {
        on_time_delivery: 92,
        fuel_efficiency: 13.2,
        customer_rating: 4.2,
        safety_score: 78,
      },
    },
  ];

  useEffect(() => {
    // In a real app, dispatch action to fetch drivers
    // dispatch(fetchDrivers());
  }, [dispatch]);

  const handleCreateDriver = () => {
    setDialogMode('create');
    setDriverForm({
      name: '',
      phone: '',
      email: '',
      license_number: '',
      license_type: '',
      license_expiry: '',
      address: '',
      emergency_contact: '',
      vehicle_assigned: '',
      status: 'available',
    });
    setOpenDialog(true);
  };

  const handleViewDriver = (driver) => {
    setSelectedDriver(driver);
    setDialogMode('view');
    setOpenDialog(true);
  };

  const handleEditDriver = (driver) => {
    setSelectedDriver(driver);
    setDriverForm({
      name: driver.name,
      phone: driver.phone,
      email: driver.email,
      license_number: driver.license_number,
      license_type: driver.license_type,
      license_expiry: driver.license_expiry,
      address: driver.address,
      emergency_contact: driver.emergency_contact,
      vehicle_assigned: driver.vehicle_assigned || '',
      status: driver.status,
    });
    setDialogMode('edit');
    setOpenDialog(true);
  };

  const handleSaveDriver = () => {
    if (dialogMode === 'create') {
      // dispatch(createDriver(driverForm));
      console.log('Creating driver:', driverForm);
    } else if (dialogMode === 'edit') {
      // dispatch(updateDriver(selectedDriver.id, driverForm));
      console.log('Updating driver:', selectedDriver.id, driverForm);
    }
    setOpenDialog(false);
  };

  const handleFormChange = (field, value) => {
    setDriverForm(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const getStatusColor = (status) => {
    const statusObj = driverStatuses.find(s => s.value === status);
    return statusObj ? statusObj.color : 'default';
  };

  const getStatusLabel = (status) => {
    const statusObj = driverStatuses.find(s => s.value === status);
    return statusObj ? statusObj.label : status;
  };

  const getDocumentStatusIcon = (status) => {
    switch (status) {
      case 'verified':
        return <CheckCircleIcon color="success" />;
      case 'pending':
        return <WarningIcon color="warning" />;
      case 'expired':
        return <BlockIcon color="error" />;
      default:
        return <WarningIcon color="warning" />;
    }
  };

  const filteredDrivers = filterStatus === 'all' 
    ? mockDrivers 
    : mockDrivers.filter(driver => driver.status === filterStatus);

  const DriverCard = ({ driver }) => (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box display="flex" alignItems="center">
            <Badge
              overlap="circular"
              anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
              badgeContent={
                <Box
                  sx={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    bgcolor: driver.status === 'available' ? 'success.main' : 
                            driver.status === 'on_trip' ? 'primary.main' :
                            driver.status === 'busy' ? 'warning.main' : 'grey.400',
                    border: '2px solid white',
                  }}
                />
              }
            >
              <Avatar sx={{ width: 56, height: 56, mr: 2 }}>
                {driver.name.split(' ').map(n => n[0]).join('')}
              </Avatar>
            </Badge>
            <Box>
              <Typography variant="h6">{driver.name}</Typography>
              <Box display="flex" alignItems="center" mt={1}>
                <Rating value={driver.rating} precision={0.1} size="small" readOnly />
                <Typography variant="body2" sx={{ ml: 1 }}>
                  ({driver.rating})
                </Typography>
              </Box>
              <Chip 
                label={getStatusLabel(driver.status)} 
                color={getStatusColor(driver.status)}
                size="small"
                sx={{ mt: 1 }}
              />
            </Box>
          </Box>
          
          <Box>
            <Tooltip title="Call Driver">
              <IconButton size="small" color="primary">
                <CallIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Send Message">
              <IconButton size="small" color="primary">
                <MessageIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="View Details">
              <IconButton size="small" onClick={() => handleViewDriver(driver)}>
                <ViewIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Edit Driver">
              <IconButton size="small" onClick={() => handleEditDriver(driver)}>
                <EditIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Box display="flex" alignItems="center" mb={1}>
              <PhoneIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2">{driver.phone}</Typography>
            </Box>
            <Box display="flex" alignItems="center" mb={1}>
              <LocationIcon color="secondary" sx={{ mr: 1 }} />
              <Typography variant="body2">{driver.current_location}</Typography>
            </Box>
            {driver.vehicle_assigned && (
              <Box display="flex" alignItems="center" mb={1}>
                <CarIcon sx={{ mr: 1 }} />
                <Typography variant="body2">{driver.vehicle_assigned}</Typography>
              </Box>
            )}
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Box display="flex" alignItems="center" mb={1}>
              <AssignmentIcon sx={{ mr: 1 }} />
              <Typography variant="body2">
                {driver.trips_completed} trips completed
              </Typography>
            </Box>
            <Box display="flex" alignItems="center" mb={1}>
              <TrendingUpIcon sx={{ mr: 1 }} />
              <Typography variant="body2">
                ₹{driver.earnings_this_month.toLocaleString()} this month
              </Typography>
            </Box>
            <Box display="flex" alignItems="center" mb={1}>
              <ScheduleIcon sx={{ mr: 1 }} />
              <Typography variant="body2">
                {driver.experience_years} years experience
              </Typography>
            </Box>
          </Grid>
        </Grid>

        {/* Performance indicators */}
        <Box mt={2}>
          <Typography variant="body2" gutterBottom>
            Performance Metrics:
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={6} md={3}>
              <Typography variant="caption">On-time Delivery</Typography>
              <LinearProgress 
                variant="determinate" 
                value={driver.performance.on_time_delivery} 
                color={driver.performance.on_time_delivery > 90 ? 'success' : 'warning'}
                sx={{ height: 6, borderRadius: 3 }}
              />
              <Typography variant="caption">{driver.performance.on_time_delivery}%</Typography>
            </Grid>
            <Grid item xs={6} md={3}>
              <Typography variant="caption">Safety Score</Typography>
              <LinearProgress 
                variant="determinate" 
                value={driver.performance.safety_score} 
                color={driver.performance.safety_score > 85 ? 'success' : 'warning'}
                sx={{ height: 6, borderRadius: 3 }}
              />
              <Typography variant="caption">{driver.performance.safety_score}%</Typography>
            </Grid>
          </Grid>
        </Box>

        {/* Document status */}
        <Box mt={2} display="flex" alignItems="center" gap={1}>
          <Typography variant="body2">Documents:</Typography>
          <Tooltip title={`License: ${driver.documents.license}`}>
            {getDocumentStatusIcon(driver.documents.license)}
          </Tooltip>
          <Tooltip title={`Aadhar: ${driver.documents.aadhar}`}>
            {getDocumentStatusIcon(driver.documents.aadhar)}
          </Tooltip>
          <Tooltip title={`PAN: ${driver.documents.pan}`}>
            {getDocumentStatusIcon(driver.documents.pan)}
          </Tooltip>
          <Tooltip title={`Medical: ${driver.documents.medical}`}>
            {getDocumentStatusIcon(driver.documents.medical)}
          </Tooltip>
        </Box>
      </CardContent>
    </Card>
  );

  const DriverDialog = () => (
    <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
      <DialogTitle>
        {dialogMode === 'create' ? 'Add New Driver' : 
         dialogMode === 'edit' ? 'Edit Driver' : 'Driver Details'}
      </DialogTitle>
      <DialogContent>
        {dialogMode === 'view' && selectedDriver ? (
          <Box>
            <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)} sx={{ mb: 2 }}>
              <Tab label="Personal Info" />
              <Tab label="Documents" />
              <Tab label="Performance" />
              <Tab label="Trip History" />
            </Tabs>
            
            {tabValue === 0 && (
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>Name:</strong> {selectedDriver.name}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>Phone:</strong> {selectedDriver.phone}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>Email:</strong> {selectedDriver.email}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>Address:</strong> {selectedDriver.address}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>License:</strong> {selectedDriver.license_number}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>License Type:</strong> {selectedDriver.license_type}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>License Expiry:</strong> {selectedDriver.license_expiry}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>Emergency Contact:</strong> {selectedDriver.emergency_contact}</Typography>
                </Grid>
              </Grid>
            )}
            
            {tabValue === 1 && (
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>Document Verification Status</Typography>
                </Grid>
                {Object.entries(selectedDriver.documents).map(([doc, status]) => (
                  <Grid item xs={12} md={6} key={doc}>
                    <Box display="flex" alignItems="center" justifyContent="space-between" p={2} border="1px solid #ddd" borderRadius={1}>
                      <Typography variant="body1">{doc.charAt(0).toUpperCase() + doc.slice(1)}</Typography>
                      <Box display="flex" alignItems="center">
                        {getDocumentStatusIcon(status)}
                        <Typography variant="body2" sx={{ ml: 1, textTransform: 'capitalize' }}>
                          {status}
                        </Typography>
                      </Box>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            )}
            
            {tabValue === 2 && (
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>Performance Metrics</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2">On-time Delivery Rate</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={selectedDriver.performance.on_time_delivery} 
                    sx={{ height: 8, borderRadius: 4, mb: 1 }}
                  />
                  <Typography variant="body2">{selectedDriver.performance.on_time_delivery}%</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2">Safety Score</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={selectedDriver.performance.safety_score} 
                    sx={{ height: 8, borderRadius: 4, mb: 1 }}
                  />
                  <Typography variant="body2">{selectedDriver.performance.safety_score}%</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>Customer Rating:</strong> {selectedDriver.performance.customer_rating}/5</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>Fuel Efficiency:</strong> {selectedDriver.performance.fuel_efficiency} km/l</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>Total Distance:</strong> {selectedDriver.total_distance.toLocaleString()} km</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1"><strong>Total Trips:</strong> {selectedDriver.trips_completed}</Typography>
                </Grid>
              </Grid>
            )}
          </Box>
        ) : (
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Full Name"
                value={driverForm.name}
                onChange={(e) => handleFormChange('name', e.target.value)}
                disabled={dialogMode === 'view'}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Phone Number"
                value={driverForm.phone}
                onChange={(e) => handleFormChange('phone', e.target.value)}
                disabled={dialogMode === 'view'}
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Email Address"
                type="email"
                value={driverForm.email}
                onChange={(e) => handleFormChange('email', e.target.value)}
                disabled={dialogMode === 'view'}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="License Number"
                value={driverForm.license_number}
                onChange={(e) => handleFormChange('license_number', e.target.value)}
                disabled={dialogMode === 'view'}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="License Type"
                select
                value={driverForm.license_type}
                onChange={(e) => handleFormChange('license_type', e.target.value)}
                disabled={dialogMode === 'view'}
              >
                {licenseTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="License Expiry Date"
                type="date"
                value={driverForm.license_expiry}
                onChange={(e) => handleFormChange('license_expiry', e.target.value)}
                InputLabelProps={{ shrink: true }}
                disabled={dialogMode === 'view'}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Address"
                multiline
                rows={2}
                value={driverForm.address}
                onChange={(e) => handleFormChange('address', e.target.value)}
                disabled={dialogMode === 'view'}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Emergency Contact"
                value={driverForm.emergency_contact}
                onChange={(e) => handleFormChange('emergency_contact', e.target.value)}
                disabled={dialogMode === 'view'}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Assigned Vehicle"
                value={driverForm.vehicle_assigned}
                onChange={(e) => handleFormChange('vehicle_assigned', e.target.value)}
                disabled={dialogMode === 'view'}
                placeholder="e.g., MH-01-AB-1234"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Status"
                select
                value={driverForm.status}
                onChange={(e) => handleFormChange('status', e.target.value)}
                disabled={dialogMode === 'view'}
              >
                {driverStatuses.map((status) => (
                  <MenuItem key={status.value} value={status.value}>
                    {status.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
          </Grid>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setOpenDialog(false)}>
          {dialogMode === 'view' ? 'Close' : 'Cancel'}
        </Button>
        {dialogMode !== 'view' && (
          <Button variant="contained" onClick={handleSaveDriver}>
            {dialogMode === 'create' ? 'Add Driver' : 'Update Driver'}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Driver Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreateDriver}
        >
          Add Driver
        </Button>
      </Box>

      {/* Filters and Stats */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="primary">
                {mockDrivers.filter(d => d.status === 'available').length}
              </Typography>
              <Typography variant="body2">Available Drivers</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="warning.main">
                {mockDrivers.filter(d => d.status === 'on_trip').length}
              </Typography>
              <Typography variant="body2">On Trip</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary">
                {mockDrivers.filter(d => d.status === 'offline').length}
              </Typography>
              <Typography variant="body2">Offline</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">
                {mockDrivers.reduce((sum, driver) => sum + driver.trips_completed, 0)}
              </Typography>
              <Typography variant="body2">Total Trips</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Filter by Status"
                select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
              >
                <MenuItem value="all">All Drivers</MenuItem>
                {driverStatuses.map((status) => (
                  <MenuItem key={status.value} value={status.value}>
                    {status.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Search Drivers"
                placeholder="Search by name, phone..."
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <Button fullWidth variant="outlined">
                Export Data
              </Button>
            </Grid>
            <Grid item xs={12} md={2}>
              <Button fullWidth variant="outlined">
                Performance Report
              </Button>
            </Grid>
            <Grid item xs={12} md={2}>
              <Button fullWidth variant="outlined" color="warning">
                Document Alerts
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Driver Cards */}
      {loading ? (
        <Box display="flex" justifyContent="center" p={4}>
          <Typography>Loading drivers...</Typography>
        </Box>
      ) : (
        <Box>
          {filteredDrivers.map((driver) => (
            <DriverCard key={driver.id} driver={driver} />
          ))}
        </Box>
      )}

      {/* Driver Dialog */}
      <DriverDialog />
    </Box>
  );
}

export default Drivers;
