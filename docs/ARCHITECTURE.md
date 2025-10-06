# 🏗️ Architecture Documentation

## Overview

EchoBlogs implements a **schema-based multitenancy** architecture using Django and django-tenants. This approach provides complete data isolation between tenants while sharing the same application codebase.

## 🎯 Architecture Principles

### 1. Data Isolation
- Each tenant has its own database schema
- Complete separation of tenant data
- No cross-tenant data access possible

### 2. Code Sharing
- Single codebase serves all tenants
- Shared application logic
- Centralized maintenance and updates

### 3. Domain-Based Routing
- Each tenant accessible via unique subdomain
- Automatic tenant resolution
- Seamless user experience

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EchoBlogs Architecture                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Public Schema │    │  Tenant Schema  │                │
│  │                 │    │                 │                │
│  │ • User Accounts │    │ • Blog Posts    │                │
│  │ • Tenant Mgmt   │    │ • Tenant Data   │                │
│  │ • Authentication│    │ • Isolated Data │                │
│  │ • Domain Mgmt   │    │                 │                │
│  └─────────────────┘    └─────────────────┘                │
│           │                       │                        │
│           └───────────┬───────────┘                        │
│                       │                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Django Application Layer                   │ │
│  │                                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │ │
│  │  │   Accounts  │  │    Blog     │  │   Tenants   │     │ │
│  │  │    App      │  │    App      │  │    App      │     │ │
│  │  │ (SHARED)    │  │ (TENANT)    │  │ (SHARED)    │     │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │ │
│  └─────────────────────────────────────────────────────────┘ │
│                       │                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Middleware Layer                           │ │
│  │                                                         │ │
│  │  • TenantMainMiddleware (django-tenants)                │ │
│  │  • Security Middleware                                 │ │
│  │  • Session Middleware                                  │ │
│  │  • Authentication Middleware                            │ │
│  └─────────────────────────────────────────────────────────┘ │
│                       │                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Database Layer                             │ │
│  │                                                         │ │
│  │  PostgreSQL Database                                    │ │
│  │  ┌─────────────────────────────────────────────────┐   │ │
│  │  │ public schema (shared data)                     │   │ │
│  │  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │   │ │
│  │  │ │   tenants   │ │    auth     │ │   domains   │ │   │ │
│  │  │ │   table     │ │   tables    │ │   table     │ │   │ │
│  │  └─────────────────────────────────────────────────┘   │ │
│  │  ┌─────────────────────────────────────────────────┐   │ │
│  │  │ tenant_1 schema (user1 data)                    │   │ │
│  │  │ ┌─────────────┐ ┌─────────────┐                │   │ │
│  │  │ │ blog_posts  │ │   other     │                │   │ │
│  │  │ │   table     │ │  tables     │                │   │ │
│  │  │ └─────────────┘ └─────────────┘                │   │ │
│  │  └─────────────────────────────────────────────────┘   │ │
│  │  ┌─────────────────────────────────────────────────┐   │ │
│  │  │ tenant_2 schema (user2 data)                    │   │ │
│  │  │ ┌─────────────┐ ┌─────────────┐                │   │ │
│  │  │ │ blog_posts  │ │   other     │                │   │ │
│  │  │ │   table     │ │  tables     │                │   │ │
│  │  │ └─────────────┘ └─────────────┘                │   │ │
│  │  └─────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Request Flow

### 1. Domain Resolution
```
User Request → Domain Resolution → Tenant Identification → Schema Routing
```

### 2. Detailed Flow
```
1. User visits: username.localhost:8000
2. TenantMainMiddleware intercepts request
3. Middleware queries Domain table for tenant
4. Sets connection to tenant schema
5. Django processes request in tenant context
6. Response returned to user
```

## 📊 Data Model Architecture

### Public Schema Models
```python
# tenants/models.py
class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(default=get_default_paid_until)
    on_trial = models.BooleanField(default=True)
    auto_create_schema = True

class Domain(DomainMixin):
    pass
```

### Tenant Schema Models
```python
# blog/models.py
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
```

## 🛠️ Component Architecture

### 1. Django Apps Structure

#### Shared Apps (Public Schema)
- **tenants**: Tenant and domain management
- **accounts**: User authentication and registration
- **django.contrib**: Core Django functionality

#### Tenant Apps (Tenant Schemas)
- **blog**: Blog post management
- **accounts**: User-specific functionality (if needed)

### 2. Middleware Stack
```python
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # Must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### 3. Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'echoblogsdb',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)
```

## 🔐 Security Architecture

### 1. Data Isolation
- **Schema-level isolation**: Each tenant has separate schema
- **No cross-tenant queries**: Impossible to access other tenant data
- **Automatic routing**: Middleware ensures correct schema access

### 2. Authentication & Authorization
- **Session-based authentication**: Django's built-in auth
- **CSRF protection**: All forms protected
- **Permission checks**: User-specific data access

### 3. Input Validation
- **Form validation**: Django forms with validation
- **Model validation**: Database-level constraints
- **Template escaping**: XSS prevention

## 🚀 Deployment Architecture

### Development Environment
```
┌─────────────────┐    ┌─────────────────┐
│   Development   │    │   PostgreSQL    │
│   Server        │◄──►│   Database      │
│   (Django)      │    │   (Local)       │
└─────────────────┘    └─────────────────┘
```

### Production Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Web Servers   │    │   PostgreSQL    │
│   (Nginx)       │◄──►│   (Django)      │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📈 Scalability Considerations

### 1. Horizontal Scaling
- **Stateless application**: No server-side session storage
- **Load balancing**: Multiple Django instances
- **Database clustering**: PostgreSQL replication

### 2. Vertical Scaling
- **Resource optimization**: Efficient queries
- **Caching**: Redis for session and cache storage
- **Connection pooling**: Database connection optimization

### 3. Tenant Scaling
- **Schema limits**: PostgreSQL schema limitations
- **Resource per tenant**: Monitoring tenant resource usage
- **Migration strategies**: Schema migration management

## 🔧 Configuration Management

### 1. Environment-Based Configuration
```python
# settings.py
import os

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key')
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://...')
```

### 2. Tenant-Specific Configuration
- **Per-tenant settings**: Customizable tenant configurations
- **Feature flags**: Tenant-specific feature enabling
- **Resource limits**: Per-tenant resource allocation

## 🧪 Testing Architecture

### 1. Test Isolation
- **Separate test database**: Isolated test environment
- **Tenant test creation**: Automated tenant setup for tests
- **Schema testing**: Tenant schema validation

### 2. Test Types
- **Unit tests**: Individual component testing
- **Integration tests**: Cross-component testing
- **End-to-end tests**: Full workflow testing

## 📊 Monitoring Architecture

### 1. Application Monitoring
- **Performance metrics**: Response times, throughput
- **Error tracking**: Exception monitoring
- **User analytics**: Usage patterns

### 2. Database Monitoring
- **Schema monitoring**: Tenant schema health
- **Query performance**: Database query optimization
- **Resource usage**: Database resource monitoring

## 🔄 Migration Strategy

### 1. Schema Migrations
- **Shared migrations**: Public schema updates
- **Tenant migrations**: Tenant schema updates
- **Rollback strategy**: Migration rollback procedures

### 2. Data Migrations
- **Tenant data migration**: Moving tenant data
- **Schema changes**: Structural changes
- **Data transformation**: Data format changes

## 📚 Best Practices

### 1. Development
- **Code organization**: Clear app separation
- **Configuration management**: Environment-based config
- **Error handling**: Comprehensive error handling

### 2. Deployment
- **Blue-green deployment**: Zero-downtime deployments
- **Database backups**: Regular backup procedures
- **Monitoring**: Comprehensive monitoring setup

### 3. Maintenance
- **Regular updates**: Framework and dependency updates
- **Security patches**: Timely security updates
- **Performance optimization**: Regular performance reviews
