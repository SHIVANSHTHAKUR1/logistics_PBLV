import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { api } from '../../services/api'

// Async thunks
export const fetchVehicles = createAsyncThunk(
  'vehicles/fetchVehicles',
  async () => {
    const response = await api.get('/vehicles')
    return response.data
  }
)

const initialState = {
  vehicles: [],
  loading: false,
  error: null,
}

const vehiclesSlice = createSlice({
  name: 'vehicles',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchVehicles.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchVehicles.fulfilled, (state, action) => {
        state.loading = false
        state.vehicles = action.payload
      })
      .addCase(fetchVehicles.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
  },
})

export const { clearError } = vehiclesSlice.actions
export default vehiclesSlice.reducer
