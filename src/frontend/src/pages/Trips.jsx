import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Stepper,
  Step,
  StepLabel,
  Fab,
  IconButton,
  Tooltip,
  LinearProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  LocalShipping as TruckIcon,
  LocationOn as LocationIcon,
  Schedule as ScheduleIcon,
  AttachMoney as MoneyIcon,
  Person as PersonIcon,
  Route as RouteIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  GpsFixed as GPSIcon,
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTrips } from '../store/slices/tripsSlice';

const tripStatuses = [
  { value: 'pending', label: 'Pending', color: 'warning' },
  { value: 'assigned', label: 'Assigned', color: 'info' },
  { value: 'in_progress', label: 'In Progress', color: 'primary' },
  { value: 'completed', label: 'Completed', color: 'success' },
  { value: 'cancelled', label: 'Cancelled', color: 'error' },
];

const loadTypes = [
  'General Cargo',
  'Electronics',
  'Furniture',
  'Food Items',
  'Construction Materials',
  'Chemicals',
  'Textiles',
  'Machinery',
  'Other',
];

function Trips() {
  const dispatch = useDispatch();
  const { trips, loading, drivers } = useSelector((state) => ({
    trips: state.trips.list || [],
    loading: state.trips.loading || false,
    drivers: state.drivers.list || [],
  }));

  const [openDialog, setOpenDialog] = useState(false);
  const [selectedTrip, setSelectedTrip] = useState(null);
  const [dialogMode, setDialogMode] = useState('create'); // 'create', 'edit', 'view'
  const [filterStatus, setFilterStatus] = useState('all');
  const [tripForm, setTripForm] = useState({
    pickup_location: '',
    delivery_location: '',
    pickup_datetime: '',
    delivery_datetime: '',
    load_details: {
      weight: '',
      type: '',
      description: '',
      value: '',
    },
    driver_id: '',
    special_instructions: '',
  });

  // Mock data for demonstration
  const mockTrips = [
    {
      id: '1',
      pickup_location: 'Mumbai, Maharashtra',
      delivery_location: 'Delhi, India',
      pickup_datetime: '2024-01-15T08:00:00',
      delivery_datetime: '2024-01-16T18:00:00',
      status: 'in_progress',
      driver_name: 'Rajesh Kumar',
      vehicle_number: 'MH-01-AB-1234',
      load_details: {
        weight: 5000,
        type: 'Electronics',
        description: 'Mobile phones and accessories',
        value: 500000,
      },
      route_optimization: {
        distance: 1400,
        estimated_time: 24,
        fuel_cost: 8400,
      },
      progress: 65,
    },
    {
      id: '2',
      pickup_location: 'Chennai, Tamil Nadu',
      delivery_location: 'Bangalore, Karnataka',
      pickup_datetime: '2024-01-16T06:00:00',
      delivery_datetime: '2024-01-16T14:00:00',
      status: 'pending',
      driver_name: null,
      vehicle_number: null,
      load_details: {
        weight: 2000,
        type: 'General Cargo',
        description: 'Office supplies and equipment',
        value: 150000,
      },
      route_optimization: {
        distance: 350,
        estimated_time: 8,
        fuel_cost: 2100,
      },
      progress: 0,
    },
    {
      id: '3',
      pickup_location: 'Pune, Maharashtra',
      delivery_location: 'Hyderabad, Telangana',
      pickup_datetime: '2024-01-14T10:00:00',
      delivery_datetime: '2024-01-15T08:00:00',
      status: 'completed',
      driver_name: 'Suresh Patil',
      vehicle_number: 'MH-12-CD-5678',
      load_details: {
        weight: 8000,
        type: 'Construction Materials',
        description: 'Steel rods and cement',
        value: 200000,
      },
      route_optimization: {
        distance: 560,
        estimated_time: 12,
        fuel_cost: 3360,
      },
      progress: 100,
    },
  ];

  useEffect(() => {
    dispatch(fetchTrips());
  }, [dispatch]);

  const handleCreateTrip = () => {
    setDialogMode('create');
    setTripForm({
      pickup_location: '',
      delivery_location: '',
      pickup_datetime: '',
      delivery_datetime: '',
      load_details: {
        weight: '',
        type: '',
        description: '',
        value: '',
      },
      driver_id: '',
      special_instructions: '',
    });
    setOpenDialog(true);
  };

  const handleViewTrip = (trip) => {
    setSelectedTrip(trip);
    setDialogMode('view');
    setOpenDialog(true);
  };

  const handleEditTrip = (trip) => {
    setSelectedTrip(trip);
    setTripForm({
      pickup_location: trip.pickup_location,
      delivery_location: trip.delivery_location,
      pickup_datetime: trip.pickup_datetime,
      delivery_datetime: trip.delivery_datetime,
      load_details: trip.load_details,
      driver_id: trip.driver_id || '',
      special_instructions: trip.special_instructions || '',
    });
    setDialogMode('edit');
    setOpenDialog(true);
  };

  const handleSaveTrip = () => {
    if (dialogMode === 'create') {
      // dispatch(createTrip(tripForm));
      console.log('Creating trip:', tripForm);
    } else if (dialogMode === 'edit') {
      // dispatch(updateTrip(selectedTrip.id, tripForm));
      console.log('Updating trip:', selectedTrip.id, tripForm);
    }
    setOpenDialog(false);
  };

  const handleFormChange = (field, value) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      setTripForm(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent],
          [child]: value,
        },
      }));
    } else {
      setTripForm(prev => ({
        ...prev,
        [field]: value,
      }));
    }
  };

  const getStatusColor = (status) => {
    const statusObj = tripStatuses.find(s => s.value === status);
    return statusObj ? statusObj.color : 'default';
  };

  const getStatusLabel = (status) => {
    const statusObj = tripStatuses.find(s => s.value === status);
    return statusObj ? statusObj.label : status;
  };

  const filteredTrips = filterStatus === 'all' 
    ? mockTrips 
    : mockTrips.filter(trip => trip.status === filterStatus);

  const TripCard = ({ trip }) => (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box>
            <Typography variant="h6" gutterBottom>
              Trip #{trip.id}
            </Typography>
            <Chip 
              label={getStatusLabel(trip.status)} 
              color={getStatusColor(trip.status)}
              size="small"
            />
          </Box>
          <Box>
            <Tooltip title="View Details">
              <IconButton size="small" onClick={() => handleViewTrip(trip)}>
                <ViewIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Edit Trip">
              <IconButton size="small" onClick={() => handleEditTrip(trip)}>
                <EditIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Track Location">
              <IconButton size="small">
                <GPSIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Box display="flex" alignItems="center" mb={1}>
              <LocationIcon color="primary" sx={{ mr: 1 }} />
              <Typography variant="body2">
                <strong>From:</strong> {trip.pickup_location}
              </Typography>
            </Box>
            <Box display="flex" alignItems="center" mb={1}>
              <LocationIcon color="secondary" sx={{ mr: 1 }} />
              <Typography variant="body2">
                <strong>To:</strong> {trip.delivery_location}
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Box display="flex" alignItems="center" mb={1}>
              <ScheduleIcon sx={{ mr: 1 }} />
              <Typography variant="body2">
                <strong>Pickup:</strong> {new Date(trip.pickup_datetime).toLocaleDateString()}
              </Typography>
            </Box>
            <Box display="flex" alignItems="center" mb={1}>
              <TruckIcon sx={{ mr: 1 }} />
              <Typography variant="body2">
                <strong>Load:</strong> {trip.load_details.weight}kg - {trip.load_details.type}
              </Typography>
            </Box>
          </Grid>
        </Grid>

        {trip.status === 'in_progress' && (
          <Box mt={2}>
            <Typography variant="body2" gutterBottom>
              Progress: {trip.progress}%
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={trip.progress} 
              sx={{ height: 8, borderRadius: 4 }}
            />
          </Box>
        )}

        {trip.driver_name && (
          <Box mt={2} display="flex" alignItems="center">
            <PersonIcon sx={{ mr: 1 }} />
            <Typography variant="body2">
              <strong>Driver:</strong> {trip.driver_name} - {trip.vehicle_number}
            </Typography>
          </Box>
        )}

        <Box mt={2} display="flex" justifyContent="space-between" alignItems="center">
          <Box display="flex" alignItems="center">
            <RouteIcon sx={{ mr: 1 }} />
            <Typography variant="body2">
              {trip.route_optimization.distance}km - {trip.route_optimization.estimated_time}hrs
            </Typography>
          </Box>
          <Box display="flex" alignItems="center">
            <MoneyIcon sx={{ mr: 1 }} />
            <Typography variant="body2" fontWeight="bold">
              ₹{trip.route_optimization.fuel_cost.toLocaleString()}
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  const CreateTripDialog = () => (
    <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
      <DialogTitle>
        {dialogMode === 'create' ? 'Create New Trip' : 
         dialogMode === 'edit' ? 'Edit Trip' : 'Trip Details'}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Pickup Location"
              value={tripForm.pickup_location}
              onChange={(e) => handleFormChange('pickup_location', e.target.value)}
              disabled={dialogMode === 'view'}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Delivery Location"
              value={tripForm.delivery_location}
              onChange={(e) => handleFormChange('delivery_location', e.target.value)}
              disabled={dialogMode === 'view'}
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Pickup Date & Time"
              type="datetime-local"
              value={tripForm.pickup_datetime}
              onChange={(e) => handleFormChange('pickup_datetime', e.target.value)}
              InputLabelProps={{ shrink: true }}
              disabled={dialogMode === 'view'}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Delivery Date & Time"
              type="datetime-local"
              value={tripForm.delivery_datetime}
              onChange={(e) => handleFormChange('delivery_datetime', e.target.value)}
              InputLabelProps={{ shrink: true }}
              disabled={dialogMode === 'view'}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Load Weight (kg)"
              type="number"
              value={tripForm.load_details.weight}
              onChange={(e) => handleFormChange('load_details.weight', e.target.value)}
              disabled={dialogMode === 'view'}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Load Type"
              select
              value={tripForm.load_details.type}
              onChange={(e) => handleFormChange('load_details.type', e.target.value)}
              disabled={dialogMode === 'view'}
            >
              {loadTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  {type}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Load Description"
              multiline
              rows={3}
              value={tripForm.load_details.description}
              onChange={(e) => handleFormChange('load_details.description', e.target.value)}
              disabled={dialogMode === 'view'}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Load Value (₹)"
              type="number"
              value={tripForm.load_details.value}
              onChange={(e) => handleFormChange('load_details.value', e.target.value)}
              disabled={dialogMode === 'view'}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Assign Driver"
              select
              value={tripForm.driver_id}
              onChange={(e) => handleFormChange('driver_id', e.target.value)}
              disabled={dialogMode === 'view'}
            >
              <MenuItem value="">Auto Assign (AI Recommendation)</MenuItem>
              {/* Mock drivers - in real app, map from drivers state */}
              <MenuItem value="1">Rajesh Kumar</MenuItem>
              <MenuItem value="2">Suresh Patil</MenuItem>
              <MenuItem value="3">Vikram Singh</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Special Instructions"
              multiline
              rows={2}
              value={tripForm.special_instructions}
              onChange={(e) => handleFormChange('special_instructions', e.target.value)}
              disabled={dialogMode === 'view'}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setOpenDialog(false)}>
          {dialogMode === 'view' ? 'Close' : 'Cancel'}
        </Button>
        {dialogMode !== 'view' && (
          <Button variant="contained" onClick={handleSaveTrip}>
            {dialogMode === 'create' ? 'Create Trip' : 'Update Trip'}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Trip Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreateTrip}
        >
          Create Trip
        </Button>
      </Box>

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
                <MenuItem value="all">All Trips</MenuItem>
                {tripStatuses.map((status) => (
                  <MenuItem key={status.value} value={status.value}>
                    {status.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Search Trips"
                placeholder="Search by location, driver..."
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Date Range"
                type="date"
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <Button fullWidth variant="outlined">
                Export Trips
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Trip Cards */}
      {loading ? (
        <Box display="flex" justifyContent="center" p={4}>
          <Typography>Loading trips...</Typography>
        </Box>
      ) : (
        <Box>
          {filteredTrips.map((trip) => (
            <TripCard key={trip.id} trip={trip} />
          ))}
        </Box>
      )}

      {/* Floating Action Button for Quick Trip Creation */}
      <Fab
        color="primary"
        aria-label="add trip"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={handleCreateTrip}
      >
        <AddIcon />
      </Fab>

      {/* Create/Edit Trip Dialog */}
      <CreateTripDialog />
    </Box>
  );
}

export default Trips;
