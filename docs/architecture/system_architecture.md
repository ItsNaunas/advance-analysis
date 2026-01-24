# FFSmart System Architecture

## Overview

The FFSmart system follows a layered architecture pattern with clear separation of concerns. The system is built using Python Flask for the backend and HTML/CSS/JavaScript for the frontend.

## Architecture Layers

### 1. Presentation Layer
- **Technology**: HTML/CSS/JavaScript with Jinja2 templates
- **Components**: 
  - Templates in `app/templates/`
  - Static files (CSS, JS) in `app/static/`
  - Responsive design for mobile and desktop

### 2. Application Layer
- **Technology**: Flask Blueprints (Controllers)
- **Components**:
  - Route handlers in `app/controllers/`
  - Request/response handling
  - Session management

### 3. Business Logic Layer
- **Technology**: Python Services
- **Components**:
  - Business logic in `app/services/`
  - Validation and business rules
  - Transaction management

### 4. Data Access Layer
- **Technology**: Repository Pattern with SQLAlchemy
- **Components**:
  - Repositories in `app/repositories/`
  - Database abstraction
  - Query optimization

### 5. Data Layer
- **Technology**: SQLite database
- **Components**:
  - SQLAlchemy models in `app/models/`
  - Database schema
  - Relationships and constraints

## Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Templates  │  │  Static CSS  │  │  Static JS   │  │
│  │   (Jinja2)   │  │              │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Auth        │  │ Inventory    │  │ Delivery     │  │
│  │ Controller  │  │ Controller   │  │ Controller   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Reorder     │  │ Notification │  │ Dashboard    │  │
│  │ Controller  │  │ Controller   │  │ Controller   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Business Logic Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Auth        │  │ Inventory    │  │ Notification │  │
│  │ Service     │  │ Service      │  │ Service      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐                                      ┌──────┐│
│  │ Reorder      │                                  │ RBAC ││
│  │ Service      │                                  │ Middle││
│  └──────────────┘                                  └──────┘│
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Data Access Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ User        │  │ Inventory    │  │ Audit        │  │
│  │ Repository  │  │ Repository   │  │ Repository   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                      Data Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Users       │  │ Inventory   │  │ Suppliers   │  │
│  │ Table       │  │ Table       │  │ Table       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Deliveries  │  │ Notifications│  │ Reorders    │  │
│  │ Table       │  │ Table       │  │ Table       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐                                      │
│  │ Audit Logs  │                                      │
│  │ Table        │                                      │
│  └──────────────┘                                      │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

1. **User Request** → Presentation Layer (Templates/Forms)
2. **Form Submission** → Application Layer (Controller)
3. **Controller** → Business Logic Layer (Service)
4. **Service** → Data Access Layer (Repository)
5. **Repository** → Data Layer (Database)
6. **Response flows back** through the layers

## Security Architecture

- **Authentication**: Flask-Login with session management
- **Authorization**: Role-Based Access Control (RBAC) middleware
- **Password Security**: bcrypt hashing
- **Session Security**: Secure cookies, CSRF protection
- **Audit Trail**: Complete logging of all actions

## Scalability Considerations

- **Database**: SQLite suitable for single-server deployment, can be migrated to PostgreSQL
- **Caching**: Can add Redis for session storage and caching
- **Load Balancing**: Stateless design allows horizontal scaling
- **Background Tasks**: APScheduler for scheduled tasks (can be upgraded to Celery)
