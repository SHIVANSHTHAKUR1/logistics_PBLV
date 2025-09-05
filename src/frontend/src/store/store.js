import { configureStore } from '@reduxjs/toolkit'
import dashboardReducer from './slices/dashboardSlice'
import tripsReducer from './slices/tripsSlice'
import driversReducer from './slices/driversSlice'
import vehiclesReducer from './slices/vehiclesSlice'
import analyticsReducer from './slices/analyticsSlice'

export const store = configureStore({
  reducer: {
    dashboard: dashboardReducer,
    trips: tripsReducer,
    drivers: driversReducer,
    vehicles: vehiclesReducer,
    analytics: analyticsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
})
