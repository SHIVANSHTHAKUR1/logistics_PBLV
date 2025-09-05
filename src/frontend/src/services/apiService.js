// API service for backend integration
const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend URL

class APIService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Trip Management APIs
  async createTrip(tripData) {
    return this.request('/trips/', {
      method: 'POST',
      body: JSON.stringify(tripData),
    });
  }

  async getTrips(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/trips/?${params}`);
  }

  async getTripById(tripId) {
    return this.request(`/trips/${tripId}`);
  }

  async updateTrip(tripId, updates) {
    return this.request(`/trips/${tripId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async deleteTrip(tripId) {
    return this.request(`/trips/${tripId}`, {
      method: 'DELETE',
    });
  }

  // Driver Management APIs
  async createDriver(driverData) {
    return this.request('/drivers/', {
      method: 'POST',
      body: JSON.stringify(driverData),
    });
  }

  async getDrivers(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/drivers/?${params}`);
  }

  async getDriverById(driverId) {
    return this.request(`/drivers/${driverId}`);
  }

  async updateDriver(driverId, updates) {
    return this.request(`/drivers/${driverId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async updateDriverStatus(driverId, status, location) {
    return this.request(`/drivers/${driverId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status, location }),
    });
  }

  // AI Agent APIs
  async getRouteOptimization(tripData) {
    return this.request('/ai/route-optimization', {
      method: 'POST',
      body: JSON.stringify(tripData),
    });
  }

  async getDriverRecommendations(tripData) {
    return this.request('/ai/driver-assignment', {
      method: 'POST',
      body: JSON.stringify(tripData),
    });
  }

  async getCostOptimization(tripData) {
    return this.request('/ai/cost-optimization', {
      method: 'POST',
      body: JSON.stringify(tripData),
    });
  }

  async getPredictiveAnalytics(filters) {
    return this.request('/ai/predictive-analytics', {
      method: 'POST',
      body: JSON.stringify(filters),
    });
  }

  // Analytics APIs
  async getDashboardStats(dateRange = '30d') {
    return this.request(`/analytics/dashboard?date_range=${dateRange}`);
  }

  async getTripAnalytics(filters) {
    return this.request('/analytics/trips', {
      method: 'POST',
      body: JSON.stringify(filters),
    });
  }

  async getDriverPerformance(filters) {
    return this.request('/analytics/drivers', {
      method: 'POST',
      body: JSON.stringify(filters),
    });
  }

  async getFinancialMetrics(filters) {
    return this.request('/analytics/financial', {
      method: 'POST',
      body: JSON.stringify(filters),
    });
  }

  async generateReport(reportType, filters) {
    return this.request('/analytics/reports', {
      method: 'POST',
      body: JSON.stringify({ type: reportType, filters }),
    });
  }

  // Real-time tracking APIs
  async getVehicleLocation(vehicleId) {
    return this.request(`/tracking/vehicle/${vehicleId}`);
  }

  async getTripProgress(tripId) {
    return this.request(`/tracking/trip/${tripId}`);
  }

  async getTrafficAlerts(route) {
    return this.request('/tracking/traffic-alerts', {
      method: 'POST',
      body: JSON.stringify({ route }),
    });
  }

  // Notification APIs
  async getNotifications(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/notifications/?${params}`);
  }

  async markNotificationRead(notificationId) {
    return this.request(`/notifications/${notificationId}/read`, {
      method: 'PATCH',
    });
  }

  async sendWhatsAppMessage(phone, message) {
    return this.request('/whatsapp/send', {
      method: 'POST',
      body: JSON.stringify({ phone, message }),
    });
  }

  // File upload APIs
  async uploadDriverDocument(driverId, documentType, file) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);

    return this.request(`/drivers/${driverId}/documents`, {
      method: 'POST',
      body: formData,
      headers: {}, // Remove Content-Type to let browser set it for FormData
    });
  }

  async uploadTripDocument(tripId, documentType, file) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);

    return this.request(`/trips/${tripId}/documents`, {
      method: 'POST',
      body: formData,
      headers: {}, // Remove Content-Type to let browser set it for FormData
    });
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }

  // WebSocket connection for real-time updates
  connectWebSocket() {
    const wsURL = this.baseURL.replace('http', 'ws') + '/ws';
    const ws = new WebSocket(wsURL);
    
    ws.onopen = () => {
      console.log('WebSocket connected');
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Handle real-time updates
      this.handleRealTimeUpdate(data);
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
      // Implement reconnection logic
      setTimeout(() => this.connectWebSocket(), 5000);
    };
    
    return ws;
  }

  handleRealTimeUpdate(data) {
    // Dispatch updates to Redux store
    const { type, payload } = data;
    
    switch (type) {
      case 'trip_progress_update':
        // Update trip progress in store
        break;
      case 'driver_location_update':
        // Update driver location in store
        break;
      case 'traffic_alert':
        // Show traffic alert notification
        break;
      case 'maintenance_alert':
        // Show maintenance alert
        break;
      default:
        console.log('Unknown real-time update type:', type);
    }
  }
}

// Create singleton instance
const apiService = new APIService();

export default apiService;

// Export individual API functions for convenience
export const {
  createTrip,
  getTrips,
  getTripById,
  updateTrip,
  deleteTrip,
  createDriver,
  getDrivers,
  getDriverById,
  updateDriver,
  updateDriverStatus,
  getRouteOptimization,
  getDriverRecommendations,
  getCostOptimization,
  getPredictiveAnalytics,
  getDashboardStats,
  getTripAnalytics,
  getDriverPerformance,
  getFinancialMetrics,
  generateReport,
  getVehicleLocation,
  getTripProgress,
  getTrafficAlerts,
  getNotifications,
  markNotificationRead,
  sendWhatsAppMessage,
  uploadDriverDocument,
  uploadTripDocument,
  healthCheck,
  connectWebSocket,
} = apiService;
