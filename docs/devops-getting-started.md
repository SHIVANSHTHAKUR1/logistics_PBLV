# Getting Started Guide - DevOps & Automation (Shivansh Thakur)

## 🎯 Your Role: DevOps & Automation Specialist

You'll be responsible for n8n workflow automation, system integration, testing coordination, deployment, and ensuring everything works together seamlessly.

---

## 🛠️ Development Environment Setup

### Step 1: Install Required Software
```bash
# Install Node.js 18+ from nodejs.org
node --version
npm --version

# Install Docker Desktop
# Download from docker.com and install

# Install Git (if not already installed)
# Download from git-scm.com

# Install VS Code
# Download from code.visualstudio.com
```

### Step 2: Install VS Code Extensions
- Docker (Microsoft)
- YAML (Red Hat)
- REST Client (for API testing)
- GitLens
- Thunder Client
- n8n Workflow Editor (if available)

### Step 3: Setup n8n Environment
```bash
# Install n8n globally
npm install n8n -g

# Or use Docker (recommended for development)
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n

# Create n8n data directory
mkdir n8n-data

# Run n8n with persistent data
docker run -it --rm --name n8n -p 5678:5678 -v n8n-data:/home/node/.n8n n8nio/n8n
```

---

## 📁 Your Folder Structure

Create these directories:
```
src/
├── automation/              # n8n workflows and configs
│   ├── workflows/          # .json workflow files
│   ├── credentials/        # API credentials (encrypted)
│   └── custom-nodes/       # Custom n8n nodes if needed
├── deployment/             # Deployment configurations
│   ├── docker/            # Docker files
│   ├── nginx/             # Web server configs
│   └── scripts/           # Deployment scripts
├── monitoring/             # System monitoring
│   ├── logs/              # Log configurations
│   └── alerts/            # Alert configurations
└── testing/               # Integration and E2E tests
    ├── api-tests/         # API testing
    ├── integration/       # Integration tests
    └── performance/       # Load testing
```

---

## 🔧 Week 1 Tasks - Environment Setup & Documentation

### Task 1: Complete Development Environment Setup
Create `docs/development-setup.md`:
```markdown
# Development Environment Setup Guide

## Prerequisites
- Python 3.9+ (for backend)
- Node.js 18+ (for frontend and n8n)
- Docker Desktop
- Git

## Backend Setup (Sanjit)
1. Create virtual environment:
   ```bash
   python -m venv logistics_env
   logistics_env\Scripts\activate  # Windows
   source logistics_env/bin/activate  # macOS/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Environment variables (.env file):
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_key
   WHATSAPP_TOKEN=your_whatsapp_token
   JWT_SECRET_KEY=your_jwt_secret
   ```

## Frontend Setup (Shashank)
1. Navigate to frontend directory:
   ```bash
   cd src/frontend
   npm install
   ```

2. Start development server:
   ```bash
   npm start
   ```

## n8n Setup (Shivansh)
1. Using Docker:
   ```bash
   docker run -d --name n8n-instance -p 5678:5678 -v n8n-data:/home/node/.n8n n8nio/n8n
   ```

2. Access n8n at: http://localhost:5678
```

### Task 2: Create Docker Development Environment
Create `deployment/docker/docker-compose.dev.yml`:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ../../
      dockerfile: deployment/docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
    volumes:
      - ../../src/backend:/app
    depends_on:
      - postgres
      - redis

  frontend:
    build:
      context: ../../
      dockerfile: deployment/docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    volumes:
      - ../../src/frontend:/app
    environment:
      - REACT_APP_API_URL=http://localhost:8000

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
    volumes:
      - n8n_data:/home/node/.n8n
      - ./automation/workflows:/home/node/.n8n/workflows

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=logistics_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  n8n_data:
  postgres_data:
```

### Task 3: Setup Project Repository Structure
Create `.gitignore` additions for your specific needs:
```gitignore
# n8n specific
n8n-data/
*.n8nworkflow.json

# Docker
.docker/
docker-compose.override.yml

# Environment specific
.env.local
.env.development
.env.production

# Logs
logs/
*.log

# Testing
coverage/
test-results/
```

---

## 🤖 Week 2 Tasks - n8n Workflow Foundation

### Task 1: Basic n8n Workflow for Driver Availability
Create your first workflow: "Driver Availability Management"

**Workflow Steps:**
1. **Webhook Trigger** - Receives WhatsApp messages
2. **Code Node** - Parses message content
3. **Condition Node** - Checks if message is availability update
4. **Database Node** - Updates driver status in Supabase
5. **WhatsApp Response** - Sends confirmation back to driver

**n8n Workflow JSON Structure:**
```json
{
  "name": "Driver Availability Management",
  "nodes": [
    {
      "name": "WhatsApp Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "parameters": {
        "path": "whatsapp-driver",
        "httpMethod": "POST"
      }
    },
    {
      "name": "Parse Message",
      "type": "n8n-nodes-base.code",
      "position": [450, 300],
      "parameters": {
        "code": "// Parse WhatsApp message\nconst message = $json.body.toUpperCase();\nconst phone = $json.from;\n\nlet status = null;\nif (message.includes('FREE') || message.includes('AVAILABLE')) {\n  status = 'available';\n} else if (message.includes('BUSY') || message.includes('OCCUPIED')) {\n  status = 'busy';\n}\n\nreturn {\n  phone: phone,\n  message: message,\n  status: status,\n  timestamp: new Date().toISOString()\n};"
      }
    }
  ],
  "connections": {
    "WhatsApp Webhook": {
      "main": [["Parse Message"]]
    }
  }
}
```

### Task 2: Setup Database Integration in n8n
Configure Supabase connection in n8n:
1. Create credential for Supabase
2. Test database connection
3. Create nodes for CRUD operations

### Task 3: Create Testing Workflow
Build a workflow to test API endpoints automatically:
```json
{
  "name": "API Health Check",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "triggerTimes": {
          "item": [
            {
              "mode": "everyMinute"
            }
          ]
        }
      }
    },
    {
      "name": "Test Backend Health",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:8000/health",
        "method": "GET"
      }
    }
  ]
}
```

---

## 🔗 Week 3-4 Tasks - Core Automation Workflows

### Task 1: Trip Assignment Workflow
Create "Automated Trip Assignment" workflow:

**Process Flow:**
1. New trip created in database (trigger)
2. Find available drivers in area
3. Send trip offer to drivers via WhatsApp
4. Wait for driver response
5. Assign trip to first driver who accepts
6. Notify owner and update dashboard

### Task 2: Document Processing Workflow
Create "Document Digitization" workflow:

**Process Flow:**
1. Driver uploads receipt image via WhatsApp
2. Save image to cloud storage
3. Extract text using OCR (integrate with backend)
4. Parse expense amount and category
5. Update trip expenses in database
6. Send confirmation to driver

Example n8n code node for OCR integration:
```javascript
// OCR Integration Node
const axios = require('axios');

// Call backend OCR endpoint
const response = await axios.post('http://localhost:8000/agents/document-digitizer', {
  image_data: $json.image_base64,
  trip_id: $json.trip_id
});

return {
  extracted_text: response.data.text,
  amount: response.data.amount,
  category: response.data.category,
  confidence: response.data.confidence
};
```

### Task 3: Financial Reporting Workflow
Create "Weekly Financial Report" workflow:

**Process Flow:**
1. Scheduled trigger (every Sunday)
2. Query database for week's data
3. Calculate profits, expenses, driver payments
4. Generate Excel report
5. Email report to owner
6. Update dashboard metrics

---

## 🧪 Week 5-6 Tasks - Testing & Quality Assurance

### Task 1: API Testing Framework
Create automated API tests using n8n:

Create `testing/api-tests/test-workflows.json`:
```json
{
  "name": "API Integration Tests",
  "nodes": [
    {
      "name": "Test User Registration",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:8000/auth/register",
        "method": "POST",
        "body": {
          "username": "testuser",
          "email": "test@example.com",
          "password": "testpass123"
        }
      }
    },
    {
      "name": "Validate Response",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "code": "if ($json.status_code !== 201) {\n  throw new Error('Registration failed');\n}\nreturn $json;"
      }
    }
  ]
}
```

### Task 2: Integration Testing Setup
Create comprehensive integration tests:

1. **WhatsApp Message Flow Test:**
   - Send test message → Verify database update → Check response

2. **Trip Assignment Test:**
   - Create trip → Verify driver notification → Test assignment

3. **Document Processing Test:**
   - Upload test image → Verify OCR → Check expense creation

### Task 3: Performance Monitoring
Setup monitoring workflows:

```javascript
// Performance Monitoring Node
const start = Date.now();

// Test API response time
const response = await $http.get('http://localhost:8000/api/v1/trips');

const responseTime = Date.now() - start;

if (responseTime > 2000) {
  // Send alert if response time > 2 seconds
  await $http.post('http://localhost:8000/alerts', {
    type: 'performance',
    message: `API response time: ${responseTime}ms`,
    severity: 'warning'
  });
}

return {
  endpoint: '/api/v1/trips',
  response_time: responseTime,
  status: response.status
};
```

---

## 🚀 Week 7-8 Tasks - Deployment & Production Setup

### Task 1: Production Environment Setup
Create `deployment/docker/docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - backend
      - frontend

  backend:
    build:
      context: ../../
      dockerfile: deployment/docker/Dockerfile.backend.prod
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - postgres
      - redis

  frontend:
    build:
      context: ../../
      dockerfile: deployment/docker/Dockerfile.frontend.prod
    environment:
      - REACT_APP_API_URL=https://yourdomain.com/api

  n8n:
    image: n8nio/n8n:latest
    environment:
      - N8N_HOST=yourdomain.com
      - N8N_PORT=443
      - N8N_PROTOCOL=https
    volumes:
      - n8n_data:/home/node/.n8n
```

### Task 2: CI/CD Pipeline Setup
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          # Run backend tests
          cd src/backend && python -m pytest
          # Run frontend tests
          cd src/frontend && npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Server
        run: |
          # Deploy using Docker Compose
          docker-compose -f deployment/docker/docker-compose.prod.yml up -d
```

---

## 📊 Monitoring & Maintenance

### Task 1: System Monitoring
Create monitoring dashboard workflows:

1. **System Health Monitor:**
   - Check all services every 5 minutes
   - Alert if any service is down
   - Log performance metrics

2. **Error Tracking:**
   - Monitor API error rates
   - Track failed workflows
   - Send alerts for critical errors

3. **Usage Analytics:**
   - Track daily active users
   - Monitor message volume
   - Report system usage statistics

### Task 2: Backup & Recovery
Create automated backup workflows:

```javascript
// Database Backup Workflow
const { exec } = require('child_process');

// Create database backup
exec('pg_dump logistics_db > backup_' + new Date().toISOString().split('T')[0] + '.sql', 
  (error, stdout, stderr) => {
    if (error) {
      throw new Error('Backup failed: ' + error.message);
    }
    return { status: 'success', backup_file: 'backup_' + new Date().toISOString().split('T')[0] + '.sql' };
  });
```

---

## 🤝 Collaboration Points

### With Sanjit (Backend):
- API endpoint testing and validation
- Database schema changes coordination  
- WhatsApp webhook integration testing
- Performance optimization

### With Shashank (Frontend):
- Real-time data update testing
- API integration verification
- User interface workflow testing
- Cross-browser compatibility

---

## 📊 Weekly Deliverables

**Week 1:**
- [ ] Development environment documentation
- [ ] Docker development setup
- [ ] Git repository structure
- [ ] Basic n8n instance running

**Week 2:**
- [ ] First n8n workflow (driver availability)
- [ ] Database integration in n8n
- [ ] API health check automation
- [ ] Testing framework setup

**Week 3:**
- [ ] Trip assignment workflow
- [ ] Document processing automation
- [ ] WhatsApp integration testing

**Week 4:**
- [ ] Financial reporting automation
- [ ] Performance monitoring setup
- [ ] Integration testing complete

**Week 5-6:**
- [ ] Comprehensive test suite
- [ ] Production environment setup
- [ ] CI/CD pipeline
- [ ] Monitoring and alerting

Remember: Your role is crucial for making sure all components work together seamlessly. Focus on automation, testing, and reliability!
