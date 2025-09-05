import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { api } from '../../services/api'

// Async thunks for API calls
export const fetchDashboardStats = createAsyncThunk(
  'dashboard/fetchStats',
  async () => {
    const response = await api.get('/dashboard/stats')
    return response.data
  }
)

export const fetchRecentActivities = createAsyncThunk(
  'dashboard/fetchActivities',
  async () => {
    const response = await api.get('/dashboard/activities')
    return response.data
  }
)

const initialState = {
  stats: {
    totalTrips: 0,
    activeTrips: 0,
    availableDrivers: 0,
    totalRevenue: 0,
    totalExpenses: 0,
    fleetUtilization: 0,
  },
  recentActivities: [],
  loading: false,
  error: null,
}

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
    updateStats: (state, action) => {
      state.stats = { ...state.stats, ...action.payload }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch stats
      .addCase(fetchDashboardStats.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchDashboardStats.fulfilled, (state, action) => {
        state.loading = false
        state.stats = action.payload
      })
      .addCase(fetchDashboardStats.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      // Fetch activities
      .addCase(fetchRecentActivities.pending, (state) => {
        state.loading = true
      })
      .addCase(fetchRecentActivities.fulfilled, (state, action) => {
        state.loading = false
        state.recentActivities = action.payload
      })
      .addCase(fetchRecentActivities.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
  },
})

export const { clearError, updateStats } = dashboardSlice.actions
export default dashboardSlice.reducer
