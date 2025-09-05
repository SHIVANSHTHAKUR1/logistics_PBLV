import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { api } from '../../services/api'

// Async thunks
export const fetchTrips = createAsyncThunk(
  'trips/fetchTrips',
  async (params = {}) => {
    const response = await api.get('/trips', { params })
    return response.data
  }
)

export const createTrip = createAsyncThunk(
  'trips/createTrip',
  async (tripData) => {
    const response = await api.post('/trips', tripData)
    return response.data
  }
)

export const updateTrip = createAsyncThunk(
  'trips/updateTrip',
  async ({ id, data }) => {
    const response = await api.put(`/trips/${id}`, data)
    return response.data
  }
)

export const createIntelligentTrip = createAsyncThunk(
  'trips/createIntelligentTrip',
  async (tripData) => {
    const response = await api.post('/ai/trips/create-intelligent', tripData)
    return response.data
  }
)

const initialState = {
  trips: [],
  list: [],
  currentTrip: null,
  loading: false,
  error: null,
  filters: {
    status: 'all',
    dateRange: null,
    driverId: null,
  },
  pagination: {
    page: 1,
    limit: 10,
    total: 0,
  },
}

const tripsSlice = createSlice({
  name: 'trips',
  initialState,
  reducers: {
    setCurrentTrip: (state, action) => {
      state.currentTrip = action.payload
    },
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload }
    },
    setPagination: (state, action) => {
      state.pagination = { ...state.pagination, ...action.payload }
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch trips
      .addCase(fetchTrips.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchTrips.fulfilled, (state, action) => {
        state.loading = false
  state.trips = action.payload.trips || action.payload
  state.list = state.trips
        state.pagination.total = action.payload.total || action.payload.length
      })
      .addCase(fetchTrips.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      // Create trip
      .addCase(createTrip.pending, (state) => {
        state.loading = true
      })
      .addCase(createTrip.fulfilled, (state, action) => {
        state.loading = false
        state.trips.unshift(action.payload)
  state.list = state.trips
      })
      .addCase(createTrip.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      // Create intelligent trip
      .addCase(createIntelligentTrip.pending, (state) => {
        state.loading = true
      })
      .addCase(createIntelligentTrip.fulfilled, (state, action) => {
        state.loading = false
        state.trips.unshift(action.payload)
  state.list = state.trips
      })
      .addCase(createIntelligentTrip.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
  },
})

export const { setCurrentTrip, setFilters, setPagination, clearError } = tripsSlice.actions
export default tripsSlice.reducer
