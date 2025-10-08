# EchoBlogs Project Flow Explanation

## Table of Contents
1. [Project Startup Flow](#project-startup-flow)
2. [Request Processing Flow](#request-processing-flow)
3. [Multi-Tenant Architecture Flow](#multi-tenant-architecture-flow)
4. [User Registration Flow](#user-registration-flow)
5. [Authentication Flow](#authentication-flow)
6. [Blog Post Creation Flow](#blog-post-creation-flow)
7. [Template Rendering Flow](#template-rendering-flow)
8. [Database Schema Flow](#database-schema-flow)
9. [File Execution Order](#file-execution-order)
10. [Complete Request Lifecycle](#complete-request-lifecycle)

---

## Project Startup Flow

### 1. Server Startup Sequence

When you run `python manage.py runserver`, here's what happens:

```
1. manage.py (Entry Point)
   ↓
2. EchoBlogs/settings.py (Configuration Loading)
   ↓
3. EchoBlogs/urls.py (Main URL Configuration)
   ↓
4. Middleware Stack Initialization
   ↓
5. Database Connection Setup
   ↓
6. Server Ready (Listening on port 8000)
```

### 2. File Execution Order During Startup

#### **Step 1: manage.py**
```python
# manage.py - Entry point
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EchoBlogs.settings')
execute_from_command_line(sys.argv)
```
- Sets the Django settings module
- Calls Django's command line interface

#### **Step 2: EchoBlogs/settings.py**
```python
# Key configurations loaded:
INSTALLED_APPS = SHARED_APPS + TENANT_APPS
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # FIRST!
    # ... other middleware
]
DATABASES = {...}  # PostgreSQL with tenant support
TENANT_MODEL = "tenants.Client"
```
- Loads all app configurations
- Sets up multi-tenant middleware (MUST be first)
- Configures database with tenant support

#### **Step 3: EchoBlogs/urls.py**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.api_urls')),  # Public schema auth APIs
    path('api/', include('blog.api_urls')),           # Tenant schema post APIs
]
```
- Defines main URL patterns
- Routes to different apps based on schema

#### **Step 4: App URLs Loading**
- **accounts/urls.py**: Public schema routes (home, login, register, logout)
- **blog/urls.py**: Tenant schema routes (post_list, post_create)

---

## Request Processing Flow

### 1. HTTP Request Lifecycle

```
Browser Request
    ↓
WSGI/ASGI Server (wsgi.py/asgi.py)
    ↓
Django Core
    ↓
TenantMainMiddleware (FIRST!)
    ↓
Other Middleware Stack
    ↓
URL Router
    ↓
View Function
    ↓
Template Rendering
    ↓
HTTP Response
```

### 2. Middleware Execution Order

```python
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # 1. Tenant detection
    'django.middleware.security.SecurityMiddleware',        # 2. Security
    'django.contrib.sessions.middleware.SessionMiddleware', # 3. Sessions
    'django.middleware.common.CommonMiddleware',            # 4. Common processing
    'django.middleware.csrf.CsrfViewMiddleware',            # 5. CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # 6. Auth
    'django.contrib.messages.middleware.MessageMiddleware',   # 7. Messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 8. Clickjacking
]
```

---

## Multi-Tenant Architecture Flow

### 1. Tenant Detection Process

```
HTTP Request: http://username.localhost:8000/blog/
    ↓
TenantMainMiddleware processes request
    ↓
Extracts domain: "username.localhost"
    ↓
Queries tenants.Domain table
    ↓
Finds matching tenant: Client(schema_name="username")
    ↓
Switches database connection to "username" schema
    ↓
Continues with tenant-specific processing
```

### 2. Schema Switching Logic

```python
# In TenantMainMiddleware (simplified)
def process_request(self, request):
    hostname = request.get_host().split(':')[0]
    
    # Check if this is a tenant domain
    if hostname != 'localhost':
        # Extract tenant name from subdomain
        tenant_name = hostname.split('.')[0]
        
        # Switch to tenant schema
        connection.set_schema_to_public()
        tenant = Client.objects.get(schema_name=tenant_name)
        connection.set_schema_to_tenant(tenant)
        
        # Set tenant on request for views to use
        request.tenant = tenant
```

### 3. Database Schema Structure

```
PostgreSQL Database: echoblogsdb
├── public (shared schema)
│   ├── auth_user (Django users)
│   ├── tenants_client (tenant info)
│   ├── tenants_domain (domain mappings)
│   └── accounts_* (if any account-specific models)
│
└── username (tenant schemas)
    ├── blog_post (user's blog posts)
    └── [other tenant-specific tables]
```

---

## User Registration Flow (API)

### 1. Registration Process Sequence

```
Client calls: POST http://localhost:8000/api/auth/register/
    ↓
TenantMainMiddleware: Detects localhost → stays on public schema
    ↓
URL Router: accounts.api_urls → register endpoint
    ↓
accounts/api_views.py: register() handles JSON
    ↓
Creates User in public schema
    ↓
Creates Client (tenant) with schema_name = username
    ↓
Creates Domain mapping: username.localhost
    ↓
Runs migrations for new tenant schema
    ↓
Auto-logs in user
    ↓
Redirects to home page
```

### 2. Registration Code Flow

```python
# accounts/views.py - register() function
def register(request):
    # 1. Check if on public schema
    if connection.schema_name != 'public':
        return error_page()
    
    if request.method == 'POST':
        # 2. Extract form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 3. Validate data
        if not username or not email or not password:
            return render_error()
        
        # 4. Create User in public schema
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password
        )
        
        # 5. Create Tenant (Client)
        tenant = Client(schema_name=username.lower(), name=username)
        tenant.save()  # This triggers schema creation!
        
        # 6. Create Domain mapping
        domain = Domain()
        domain.domain = f"{username.lower()}.localhost"
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()
        
# 7. Issue JWT tokens in response JSON
        return Response({"user": user_data, "domain": domain, "tokens": tokens}, status=201)
```

---

## Authentication Flow (JWT)

### 1. Login Process

```
Client calls: POST http://localhost:8000/api/auth/login/
    ↓
TenantMainMiddleware: localhost → public schema
    ↓
URL Router: accounts.api_urls → login endpoint
    ↓
accounts/api_views.py: returns `{ user, tokens }`
```

### 2. Session Management

```python
# accounts/views.py - user_login() function
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user:
            # Create session
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, "accounts/login.html")
```

---

## Blog Post Creation Flow (API)

### 1. Post Creation Process

```
Client calls: http://username.localhost:8000/api/posts/
    ↓
TenantMainMiddleware: Detects username.localhost
    ↓
Queries Domain table → finds tenant
    ↓
Switches to username schema
    ↓
URL Router: blog.api_urls → posts endpoints
    ↓
blog/api_views.py: DRF views handle CRUD with JWT auth
    ↓
Creates Post in tenant schema
    ↓
Redirects to post list
```

### 2. Post Creation Code Flow

```python
# blog/views.py - post_create() function
@login_required
def post_create(request):
    if request.method == 'POST':
        # 1. Extract form data
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # 2. Validate data
        if title and content:
            # 3. Create post in CURRENT tenant schema
            Post.objects.create(
                title=title, 
                content=content, 
                author=request.user
            )
            messages.success(request, 'Post created successfully!')
            return redirect('post_list')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    # 4. Render form template
    return render(request, 'accounts/blog/post_create.html')
```

---

## API Interaction Flow

Clients call JSON endpoints under `/api`, sending `Authorization: Bearer <token>` for protected routes. Tenant isolation is enforced by domain (`<username>.localhost`).

### 3. Template Context Flow

```python
# Example: post_list view
def post_list(request):
    # 1. Query posts from CURRENT tenant schema
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    
    # 2. Create context dictionary
    context = {'posts': posts}
    
    # 3. Render template with context
    return render(request, 'accounts/blog/post_list.html', context)
```

---

## Database Schema Flow

### 1. Schema Creation Process

```
User registration triggers:
    ↓
Client.save() called
    ↓
django-tenants detects auto_create_schema = True
    ↓
Creates new PostgreSQL schema: username
    ↓
Runs migrations for tenant apps (blog)
    ↓
Creates blog_post table in username schema
    ↓
Schema ready for use
```

### 2. Schema Switching During Requests

```python
# Simplified schema switching logic
def process_request(self, request):
    hostname = request.get_host().split(':')[0]
    
    if hostname == 'localhost':
        # Public schema - shared data
        connection.set_schema_to_public()
    else:
        # Tenant schema - isolated data
        tenant_name = hostname.split('.')[0]
        tenant = Client.objects.get(schema_name=tenant_name)
        connection.set_schema_to_tenant(tenant)
```

---

## File Execution Order

### 1. Server Startup Files (in order)

```
1. manage.py                    # Entry point
2. EchoBlogs/__init__.py        # Project initialization
3. EchoBlogs/settings.py         # Configuration
4. EchoBlogs/urls.py            # Main URL routing
5. accounts/__init__.py         # App initialization
6. accounts/api_urls.py        # Auth API URL patterns
7. blog/__init__.py            # App initialization
8. blog/api_urls.py            # Post API URL patterns
9. tenants/__init__.py         # App initialization
10. tenants/models.py           # Tenant models
11. blog/models.py             # Blog models
12. accounts/models.py         # Account models
13. wsgi.py/asgi.py            # WSGI/ASGI application
```

### 2. Request Processing Files (per request)

```
1. wsgi.py/asgi.py             # Request entry point
2. EchoBlogs/settings.py       # Load settings
3. EchoBlogs/urls.py           # Main URL routing
4. TenantMainMiddleware        # Tenant detection
5. Other Middleware            # Security, sessions, etc.
6. accounts/api_urls.py OR blog/api_urls.py  # API routing
7. accounts/api_views.py OR blog/api_views.py # API view handlers
8. accounts/models.py OR blog/models.py # Database queries
9. Response sent to client (JSON)
```

---

## Complete Request Lifecycle

### 1. User Registration Request (API)

```
Client: POST http://localhost:8000/api/auth/register/
    ↓
WSGI Server (wsgi.py)
    ↓
Django Core loads settings.py
    ↓
TenantMainMiddleware: localhost → public schema
    ↓
URL Router: EchoBlogs/urls.py → accounts.api_urls
    ↓
accounts/api_views.py: register endpoint
    ↓
Validate JSON payload
    ↓
Create user (public schema)
    ↓
Create tenant schema + domain mapping
    ↓
Return JSON { user, domain, tokens } with 201
```

### 2. Blog Post Creation Request (API)

```
Client: POST http://<username>.localhost:8000/api/posts/
    ↓
WSGI Server (wsgi.py)
    ↓
Django Core loads settings.py
    ↓
TenantMainMiddleware: <username>.localhost → tenant schema
    ↓
URL Router: EchoBlogs/urls.py → blog.api_urls
    ↓
blog/api_views.py: create post (JWT required)
    ↓
Validate JSON payload and permissions
    ↓
Create Post in tenant schema
    ↓
Return 201 with post JSON
```

---

## Key Concepts Summary

### 1. **Multi-Tenant Architecture**
- Each user gets their own database schema
- Complete data isolation between tenants
- Domain-based tenant detection

### 2. **Schema Management**
- Public schema: shared data (users, tenants, domains)
- Tenant schemas: isolated data (blog posts per user)
- Automatic schema creation during registration

### 3. **Request Flow**
- TenantMainMiddleware detects tenant from domain
- Switches database connection to appropriate schema
- Views operate on correct schema automatically

### 4. **Authentication**
- Session-based authentication
- Users stored in public schema
- Sessions work across all tenant domains

### 5. **Template System**
- Base template with inheritance
- Context variables from views
- Bootstrap-based responsive design

This flow ensures that each user has their own isolated blog space while sharing the authentication system and maintaining clean separation of concerns.
