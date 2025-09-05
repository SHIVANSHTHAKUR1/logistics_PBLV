import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { api } from '../../services/api'

// Async thunks
export const fetchDrivers = createAsyncThunk(
  'drivers/fetchDrivers',
  async () => {
    const response = await api.get('/drivers')
    return response.data
  }
)

export const fetchDriverAnalytics = createAsyncThunk(
  'drivers/fetchAnalytics',
  async () => {
    const response = await api.get('/ai/drivers/analytics')
    return response.data
  }
)

export const updateDriverAvailability = createAsyncThunk(
  'drivers/updateAvailability',
  async ({ driverId, availability }) => {
    const response = await api.put(`/ai/drivers/${driverId}/availability`, { availability })
    return response.data
  }
)

const initialState = {
  drivers: [],
  list: [],
  analytics: {
    totalDrivers: 0,
    availableDrivers: 0,
    busyDrivers: 0,
    topPerformers: [],
    performanceMetrics: {},
  },
  loading: false,
  error: null,
}

const driversSlice = createSlice({
  name: 'drivers',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
    updateDriverStatus: (state, action) => {
      const { driverId, status } = action.payload
      const driver = state.drivers.find(d => d.driver_id === driverId)
      if (driver) {
        driver.availability_status = status
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch drivers
      .addCase(fetchDrivers.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchDrivers.fulfilled, (state, action) => {
        state.loading = false
  state.drivers = action.payload
  state.list = action.payload
      })
      .addCase(fetchDrivers.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      // Fetch analytics
      .addCase(fetchDriverAnalytics.fulfilled, (state, action) => {
        state.analytics = action.payload
      })
      // Update availability
      .addCase(updateDriverAvailability.fulfilled, (state, action) => {
        const driver = state.drivers.find(d => d.driver_id === action.payload.driver_id)
        if (driver) {
          driver.availability_status = action.payload.availability_status
        }
      })
  },
})

export const { clearError, updateDriverStatus } = driversSlice.actions
export default driversSlice.reducer
