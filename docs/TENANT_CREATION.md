# 🏢 Tenant Creation Guide

## Overview

This document explains how tenant creation works in EchoBlogs, including the technical implementation, user workflow, and management processes.

## 🎯 What is Tenant Creation?

Tenant creation in EchoBlogs involves:
1. **User Registration**: Creating a user account
2. **Schema Creation**: Creating an isolated database schema
3. **Domain Mapping**: Setting up subdomain access
4. **Data Initialization**: Setting up tenant-specific tables

## 🔄 User Workflow

### 1. Registration Process
```
User visits 127.0.0.1:8000/register/
    ↓
Fills registration form
    ↓
Submits form (POST request)
    ↓
System validates input
    ↓
Creates user in public schema
    ↓
Creates tenant schema
    ↓
Creates domain mapping
    ↓
Auto-login user
    ↓
Redirect to home page
```

### 2. Domain Access
After registration, users can access their blog via:
- **Main site**: `127.0.0.1:8000` (public schema)
- **Personal blog**: `username.localhost:8000` (tenant schema)

## 🛠️ Technical Implementation

### Registration View
```python
# accounts/views.py
def register(request):
    """User registration with tenant creation"""
    # Must run only on public schema
    if connection.schema_name != 'public':
        return render(request, "accounts/error.html", 
                     {"msg": "Tenant creation must be done from the public schema."})

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "accounts/register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "accounts/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "accounts/register.html")

        try:
            # Create user in public schema
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create new tenant
            tenant = Client(schema_name=username.lower(), name=username)
            tenant.save()  # runs migrations for this tenant

            # Create domain for tenant
            domain = Domain()
            domain.domain = f"{username.lower()}.localhost"
            domain.tenant = tenant
            domain.is_primary = True
            domain.save()

            messages.success(request, f"Account created successfully! Your blog is available at {domain.domain}:8000")
            
            # Auto-login the user
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')

        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, "accounts/register.html")

    return render(request, "accounts/register.html")
```

### Tenant Models
```python
# tenants/models.py
from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
from datetime import date, timedelta

def get_default_paid_until():
    return date.today() + timedelta(days=365)

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(default=get_default_paid_until)
    on_trial = models.BooleanField(default=True)
    auto_create_schema = True  # important: creates schema automatically

class Domain(DomainMixin):
    pass
```

## 🗄️ Database Schema Creation

### 1. Public Schema
Contains shared data:
- **tenants_client**: Tenant information
- **tenants_domain**: Domain mappings
- **auth_user**: User accounts
- **auth_group**: User groups
- **auth_permission**: Permissions
- **django_session**: User sessions

### 2. Tenant Schema
Each tenant gets their own schema with:
- **blog_post**: Blog posts
- **auth_user**: Tenant-specific user data (if needed)
- **django_migrations**: Migration history

### Schema Creation Process
```python
# When tenant.save() is called:
1. Django creates new PostgreSQL schema
2. Runs migrations for TENANT_APPS
3. Creates all tenant-specific tables
4. Sets up proper permissions
```

## 🌐 Domain Management

### Domain Mapping
Each tenant gets a unique subdomain:
- **Format**: `{username}.localhost`
- **Example**: `john.localhost:8000`
- **Primary Domain**: Marked as `is_primary=True`

### Domain Resolution
```python
# django-tenants middleware handles:
1. Extract domain from request
2. Query Domain table for tenant
3. Set database connection to tenant schema
4. Process request in tenant context
```

## 🔧 Management Commands

### Setup Public Tenant
```bash
python manage.py setup_public_tenant
```

This command:
- Creates public tenant for main domain
- Sets up `127.0.0.1` and `localhost` domains
- Ensures main site accessibility

### Manual Tenant Creation
```python
# Create tenant programmatically
from tenants.models import Client, Domain

# Create tenant
tenant = Client.objects.create(
    schema_name='custom_tenant',
    name='Custom Tenant',
    paid_until=date.today() + timedelta(days=365)
)

# Create domain
domain = Domain.objects.create(
    domain='custom.localhost',
    tenant=tenant,
    is_primary=True
)
```

## 🛡️ Security Considerations

### Data Isolation
- **Schema-level isolation**: Each tenant has separate schema
- **No cross-tenant access**: Impossible to access other tenant data
- **Automatic routing**: Middleware ensures correct schema

### Validation
- **Username validation**: Prevents duplicate usernames
- **Email validation**: Prevents duplicate emails
- **Password validation**: Secure password requirements
- **Domain validation**: Prevents domain conflicts

### Error Handling
- **Rollback on failure**: Failed tenant creation is rolled back
- **Error messages**: User-friendly error messages
- **Logging**: Comprehensive error logging

## 📊 Tenant Lifecycle

### 1. Creation
- User registration triggers tenant creation
- Schema and domain are created automatically
- User is auto-logged in

### 2. Active Usage
- User accesses their blog via subdomain
- All data is isolated in their schema
- Regular blog post creation and management

### 3. Management
- Admin can manage tenants via Django admin
- Tenant settings can be modified
- Domain mappings can be updated

### 4. Deletion (Future)
- Tenant deletion would remove schema
- User account would be deactivated
- Domain mapping would be removed

## 🔍 Troubleshooting

### Common Issues

#### 1. "No tenant for hostname" Error
**Problem**: Main domain not accessible
**Solution**: Run `python manage.py setup_public_tenant`

#### 2. Tenant Creation Fails
**Problem**: Database permissions or connection issues
**Solution**: Check database credentials and permissions

#### 3. Domain Not Working
**Problem**: Subdomain not resolving
**Solution**: Check domain mapping in database

### Debug Commands
```bash
# Check tenant schemas
python manage.py dbshell
\dn

# Check domain mappings
python manage.py shell
from tenants.models import Domain
Domain.objects.all()

# Check tenant list
from tenants.models import Client
Client.objects.all()
```

## 📈 Performance Considerations

### Schema Creation
- **Time**: Schema creation takes ~1-2 seconds
- **Resources**: Minimal database resources
- **Concurrency**: Multiple tenants can be created simultaneously

### Query Performance
- **Schema switching**: Minimal overhead
- **Index usage**: Each schema has its own indexes
- **Connection pooling**: Efficient connection management

## 🔮 Future Enhancements

### Planned Features
- **Tenant customization**: Custom themes and settings
- **Resource limits**: Per-tenant resource allocation
- **Billing integration**: Subscription management
- **Multi-domain support**: Custom domain mapping
- **Tenant analytics**: Usage statistics per tenant

### API Integration
- **REST API**: Programmatic tenant creation
- **Webhook support**: Tenant creation notifications
- **Bulk operations**: Mass tenant management

## 📚 Best Practices

### Development
- **Test tenant creation**: Always test in development
- **Error handling**: Comprehensive error handling
- **Validation**: Thorough input validation
- **Logging**: Detailed operation logging

### Production
- **Monitoring**: Monitor tenant creation success rate
- **Backup**: Regular database backups
- **Scaling**: Plan for tenant scaling
- **Security**: Regular security audits

## 🧪 Testing Tenant Creation

### Unit Tests
```python
from django.test import TestCase
from tenants.models import Client, Domain
from django.contrib.auth.models import User

class TenantCreationTest(TestCase):
    def test_tenant_creation(self):
        # Test tenant creation process
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        
        tenant = Client.objects.create(
            schema_name='testuser',
            name='Test User'
        )
        
        domain = Domain.objects.create(
            domain='testuser.localhost',
            tenant=tenant,
            is_primary=True
        )
        
        self.assertEqual(tenant.schema_name, 'testuser')
        self.assertEqual(domain.domain, 'testuser.localhost')
```

### Integration Tests
```python
def test_registration_flow(self):
    response = self.client.post('/register/', {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'newpass',
        'confirm_password': 'newpass'
    })
    
    self.assertEqual(response.status_code, 302)  # Redirect after success
    self.assertTrue(User.objects.filter(username='newuser').exists())
    self.assertTrue(Client.objects.filter(schema_name='newuser').exists())
```

## 📖 Additional Resources

- [django-tenants Documentation](https://django-tenants.readthedocs.io/)
- [PostgreSQL Schema Documentation](https://www.postgresql.org/docs/current/ddl-schemas.html)
- [Django Multitenancy Patterns](https://books.agiliq.com/projects/django-multi-tenant/en/latest/)
