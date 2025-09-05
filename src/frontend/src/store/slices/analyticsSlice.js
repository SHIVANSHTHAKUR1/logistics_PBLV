import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { api } from '../../services/api'

// Async thunks
export const fetchExpenseAnalytics = createAsyncThunk(
  'analytics/fetchExpenseAnalytics',
  async (params = {}) => {
    const response = await api.get('/expenses/analytics', { params })
    return response.data
  }
)

export const fetchRouteOptimization = createAsyncThunk(
  'analytics/fetchRouteOptimization',
  async (routeData) => {
    const response = await api.post('/ai/routes/optimize', routeData)
    return response.data
  }
)

const initialState = {
  expenses: {
    total: 0,
    breakdown: {},
    trends: [],
  },
  routes: {
    optimizedRoutes: [],
    suggestions: [],
  },
  performance: {
    driverMetrics: [],
    vehicleMetrics: [],
    profitability: {},
  },
  loading: false,
  error: null,
}

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Expense analytics
      .addCase(fetchExpenseAnalytics.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchExpenseAnalytics.fulfilled, (state, action) => {
        state.loading = false
        state.expenses = action.payload
      })
      .addCase(fetchExpenseAnalytics.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      // Route optimization
      .addCase(fetchRouteOptimization.fulfilled, (state, action) => {
        state.routes.optimizedRoutes.push(action.payload)
      })
  },
})

export const { clearError } = analyticsSlice.actions
export default analyticsSlice.reducer
