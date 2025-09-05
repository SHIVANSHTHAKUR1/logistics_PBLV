import axios from 'axios'

// Create axios instance with default config
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API service functions
export const dashboardService = {
  getStats: () => api.get('/dashboard/stats'),
  getActivities: () => api.get('/dashboard/activities'),
}

export const tripService = {
  getTrips: (params) => api.get('/trips', { params }),
  createTrip: (data) => api.post('/trips', data),
  updateTrip: (id, data) => api.put(`/trips/${id}`, data),
  deleteTrip: (id) => api.delete(`/trips/${id}`),
  createIntelligentTrip: (data) => api.post('/ai/trips/create-intelligent', data),
}

export const driverService = {
  getDrivers: () => api.get('/drivers'),
  createDriver: (data) => api.post('/drivers', data),
  updateDriver: (id, data) => api.put(`/drivers/${id}`, data),
  getDriverAnalytics: () => api.get('/ai/drivers/analytics'),
  updateAvailability: (id, availability) => api.put(`/ai/drivers/${id}/availability`, { availability }),
}

export const vehicleService = {
  getVehicles: () => api.get('/vehicles'),
  createVehicle: (data) => api.post('/vehicles', data),
  updateVehicle: (id, data) => api.put(`/vehicles/${id}`, data),
}

export const expenseService = {
  getExpenses: (params) => api.get('/expenses', { params }),
  createExpense: (data) => api.post('/expenses', data),
  getAnalytics: (params) => api.get('/expenses/analytics', { params }),
}

export const aiService = {
  optimizeRoute: (data) => api.post('/ai/routes/optimize', data),
  processDocument: (file) => {
    const formData = new FormData()
    formData.append('document', file)
    return api.post('/ai/documents/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  getTripIntelligence: (tripId) => api.get(`/ai/trips/${tripId}/intelligence`),
}
