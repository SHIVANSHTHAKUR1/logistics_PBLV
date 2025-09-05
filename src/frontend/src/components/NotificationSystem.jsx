import React, { useState, useEffect } from 'react';
import {
  Snackbar,
  Alert,
  IconButton,
  Typography,
  Box,
  Slide,
} from '@mui/material';
import {
  Close as CloseIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';

const NotificationSystem = () => {
  const [notifications, setNotifications] = useState([]);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const websocket = new WebSocket('ws://localhost:8000/ws');
    
    websocket.onopen = () => {
      console.log('Notification WebSocket connected');
      setWs(websocket);
    };
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleRealTimeNotification(data);
    };
    
    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    websocket.onclose = () => {
      console.log('WebSocket disconnected');
      setWs(null);
      // Attempt to reconnect after 5 seconds
      setTimeout(initializeWebSocket, 5000);
    };

    const initializeWebSocket = () => {
      if (!ws) {
        const newWs = new WebSocket('ws://localhost:8000/ws');
        setWs(newWs);
      }
    };

    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  }, []);

  const handleRealTimeNotification = (data) => {
    const notification = {
      id: Date.now() + Math.random(),
      type: data.type || 'info',
      title: data.title,
      message: data.message,
      timestamp: new Date().toISOString(),
      duration: data.duration || 6000,
      actions: data.actions || [],
    };

    setNotifications(prev => [...prev, notification]);

    // Auto-remove notification after duration
    setTimeout(() => {
      removeNotification(notification.id);
    }, notification.duration);
  };

  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const getIcon = (type) => {
    switch (type) {
      case 'success':
        return <SuccessIcon />;
      case 'warning':
        return <WarningIcon />;
      case 'error':
        return <ErrorIcon />;
      default:
        return <InfoIcon />;
    }
  };

  const getSeverity = (type) => {
    switch (type) {
      case 'success':
        return 'success';
      case 'warning':
        return 'warning';
      case 'error':
        return 'error';
      default:
        return 'info';
    }
  };

  // Function to manually add notifications (for testing or other components)
  const addNotification = (notification) => {
    handleRealTimeNotification(notification);
  };

  // Mock real-time notifications for demo
  useEffect(() => {
    const mockNotifications = [
      {
        type: 'success',
        title: 'Trip Completed',
        message: 'Trip T001 has been delivered successfully to Delhi',
        duration: 5000,
      },
      {
        type: 'warning',
        title: 'Traffic Alert',
        message: 'Heavy traffic detected on Mumbai-Pune route. ETA increased by 30 minutes.',
        duration: 7000,
      },
      {
        type: 'info',
        title: 'Driver Check-in',
        message: 'Rajesh Kumar checked in at fuel station - Highway NH-48',
        duration: 4000,
      },
      {
        type: 'error',
        title: 'Vehicle Alert',
        message: 'Vehicle MH-12-AB-3456 requires immediate maintenance check',
        duration: 8000,
      },
    ];

    // Simulate receiving notifications every 10 seconds
    let index = 0;
    const interval = setInterval(() => {
      if (index < mockNotifications.length) {
        handleRealTimeNotification(mockNotifications[index]);
        index++;
      } else {
        clearInterval(interval);
      }
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <Box>
      {notifications.map((notification, index) => (
        <Snackbar
          key={notification.id}
          open={true}
          anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
          sx={{ 
            mt: index * 7, // Stack notifications
            maxWidth: 400,
          }}
          TransitionComponent={Slide}
          TransitionProps={{ direction: 'left' }}
        >
          <Alert
            severity={getSeverity(notification.type)}
            icon={getIcon(notification.type)}
            action={
              <IconButton
                size="small"
                color="inherit"
                onClick={() => removeNotification(notification.id)}
              >
                <CloseIcon fontSize="small" />
              </IconButton>
            }
            sx={{ width: '100%' }}
          >
            <Box>
              <Typography variant="subtitle2" fontWeight="bold">
                {notification.title}
              </Typography>
              <Typography variant="body2">
                {notification.message}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {new Date(notification.timestamp).toLocaleTimeString()}
              </Typography>
            </Box>
          </Alert>
        </Snackbar>
      ))}
    </Box>
  );
};

export default NotificationSystem;

// Export the function to add notifications manually
export { NotificationSystem };
