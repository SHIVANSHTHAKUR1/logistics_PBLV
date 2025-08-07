# Project Plan - PBL-V

## Project Information
- **Project Title:** Agentic Automation for Fragmented Logistics
- **Project Code:** 22AI014
- **Team Members:** 
  - Sanjit Palial (2310993924)
  - Shashank Kumar Pathania (2310993930)
  - Shivansh Thakur (2310993931)
- **Supervisor:** Dr. Harshvardhan
- **Institution:** Chitkara University Institute of Engineering & Technology
- **Program:** Bachelor of Engineering - Computer Science & Engineering (Artificial Intelligence)
- **Semester:** 5
- **Duration:** Academic Year 2024-25
- **Start Date:** January 2025
- **End Date:** May 2025

## Project Objectives
1. **Primary Objective:** Develop an AI-powered, agent-based system that automates logistics workflow for small transport businesses and independent truck owners
2. **Secondary Objective:** Create a dual-interface solution (WhatsApp for drivers, web dashboard for owners) to ensure maximum accessibility and adoption
3. **Additional Objectives:**
   - Automate load discovery, trip assignment, expense tracking, and financial reporting
   - Improve operational efficiency and transparency in the fragmented logistics sector
   - Provide data-driven insights for better business decision making

## Scope
### In Scope
- **Driver WhatsApp Bot:** Simple message-based interface for drivers to interact with the system
- **Owner Web Dashboard:** React.js-based comprehensive management interface for transport owners
- **Automation Engine:** n8n-powered workflow automation for logistics operations
- **Central Database:** Secure backend using Supabase/Firebase for data storage
- **Intelligent Agents:**
  - Availability Agent (driver status management)
  - Marketplace Agent (load discovery and matching)
  - Dispatch Agent (automated trip assignment)
  - Document Digitizer Agent (OCR for document processing)
  - Reporting Agent (automated financial reports)
- **Core Features:**
  - Load discovery automation
  - Trip assignment and tracking
  - Expense management
  - Real-time profit/loss tracking
  - Document digitization
  - Automated reporting

### Out of Scope
- Integration with third-party logistics platforms (Phase 2)
- Mobile native applications for drivers
- Advanced AI/ML analytics and predictive modeling
- Multi-language support beyond English/Hindi
- Integration with government transport portals

## Timeline
| Phase | Task | Duration | Start Date | End Date | Status |
|-------|------|----------|------------|----------|--------|
| 1 | Requirements Analysis & System Design | 3 weeks | Jan 15, 2025 | Feb 5, 2025 | Not Started |
| 2 | Technology Setup & Environment Configuration | 1 week | Feb 6, 2025 | Feb 12, 2025 | Not Started |
| 3 | Backend Development (FastAPI + Database) | 4 weeks | Feb 13, 2025 | Mar 12, 2025 | Not Started |
| 4 | WhatsApp Bot Development | 3 weeks | Mar 13, 2025 | Apr 2, 2025 | Not Started |
| 5 | Web Dashboard Development (React.js) | 4 weeks | Mar 20, 2025 | Apr 16, 2025 | Not Started |
| 6 | Automation Engine Integration (n8n) | 2 weeks | Apr 3, 2025 | Apr 16, 2025 | Not Started |
| 7 | Intelligent Agents Development | 3 weeks | Apr 10, 2025 | Apr 30, 2025 | Not Started |
| 8 | Testing & Integration | 2 weeks | May 1, 2025 | May 14, 2025 | Not Started |
| 9 | Documentation & Final Presentation | 1 week | May 15, 2025 | May 21, 2025 | Not Started |

## Resources Required
### Technical Resources
**Programming Languages & Frameworks:**
- Python (Backend development, AI agents)
- JavaScript/React.js (Frontend dashboard)
- FastAPI (Backend API development)

**AI/ML Libraries:**
- LangChain (AI agent framework)
- LangGraph (Multi-agent workflows)
- Hugging Face Transformers (NLP models)

**Tools & Platforms:**
- n8n (Workflow automation engine)
- Supabase/Firebase (Database and backend services)
- WhatsApp Business API (Bot integration)
- OCR libraries for document processing

**Development Environment:**
- VS Code/PyCharm (Development IDE)
- Git/GitHub (Version control)
- Docker (Containerization)
- Postman (API testing)

### Human Resources
**Team Roles & Responsibilities:**
- **Sanjit Palial:** Backend development, AI agents, database design
- **Shashank Kumar Pathania:** Frontend development, UI/UX design, WhatsApp integration
- **Shivansh Thakur:** Automation workflows, testing, system integration
- **Dr. Harshvardhan:** Project supervision, technical guidance, review

**Required Skills:**
- Python programming and FastAPI
- React.js and modern web development
- AI/ML concepts and LangChain framework
- Database design and management
- API development and integration

## Risk Assessment
| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|-------------------|
| WhatsApp API limitations/changes | Medium | High | Research alternative messaging platforms, implement fallback solutions |
| Complex AI agent integration | High | Medium | Start with simple rule-based agents, gradually add AI capabilities |
| Low user adoption due to tech barriers | Medium | High | Extensive user testing, simplified interfaces, user training materials |
| Database scalability issues | Low | Medium | Use cloud-based solutions, implement proper indexing and optimization |
| Team member availability conflicts | Medium | Medium | Regular communication, flexible task allocation, backup plans |
| Integration complexity between components | High | High | Modular development approach, extensive testing, documentation |

## Success Criteria
- **Functional System:** Complete working system with all core components (WhatsApp bot, web dashboard, automation engine, intelligent agents)
- **User Interface Quality:** Intuitive and responsive web dashboard with real-time data updates
- **Automation Effectiveness:** Successfully automate at least 80% of manual logistics processes identified in problem statement
- **Integration Success:** Seamless integration between WhatsApp interface, web dashboard, and backend systems
- **Performance Standards:** System handles concurrent users and processes data efficiently
- **Documentation Completeness:** Comprehensive technical documentation, user manuals, and project report
- **Demonstration Readiness:** Working prototype ready for final presentation and evaluation

## Deliverables
1. **Technical Deliverables:**
   - Complete source code repository
   - Working web application (React.js dashboard)
   - WhatsApp bot integration
   - Database schema and setup scripts
   - Automation workflows (n8n configurations)

2. **Documentation:**
   - Technical specification document
   - User manual for both drivers and owners
   - System architecture document
   - API documentation
   - Final project report

3. **Presentation Materials:**
   - Final project presentation
   - Demo video
   - System flowchart and diagrams

## Review and Approval
- **Prepared by:** Sanjit Palial, Shashank Kumar Pathania, Shivansh Thakur
- **Review Date:** January 15, 2025
- **Approved by:** Dr. Harshvardhan
- **Approval Date:** January 20, 2025
- **Next Review Date:** February 15, 2025
