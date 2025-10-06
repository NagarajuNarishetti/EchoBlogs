# 🔗 Endpoints Documentation

## Overview

This document provides a comprehensive list of all available endpoints in EchoBlogs, including their methods, parameters, responses, and usage examples.

## 🌐 Base URLs

- **Development**: `http://127.0.0.1:8000`
- **Production**: `https://yourdomain.com`
- **Tenant Access**: `http://username.localhost:8000` (for tenant-specific endpoints)

## 📋 Endpoint Categories

### 1. Public Endpoints (Main Domain)
### 2. Authentication Endpoints
### 3. Blog Endpoints (Tenant-Specific)
### 4. Admin Endpoints

---

## 🏠 Public Endpoints

### Home Page
- **URL**: `/`
- **Method**: `GET`
- **Description**: Landing page with feature highlights and call-to-action buttons
- **Authentication**: Not required
- **Template**: `home.html`
- **Response**: HTML page

**Example Request**:
```bash
curl -X GET http://127.0.0.1:8000/
```

**Response**: Beautiful landing page with:
- Hero section with EchoBlogs branding
- Feature highlights (Data Isolation, Easy Setup, Custom Domains)
- How it works section
- Call-to-action buttons for registration/login

---

## 🔐 Authentication Endpoints

### User Registration
- **URL**: `/register/`
- **Method**: `GET`, `POST`
- **Description**: User registration with automatic tenant creation
- **Authentication**: Not required
- **Template**: `accounts/register.html`

#### GET Request
**Description**: Display registration form
**Response**: HTML registration form

#### POST Request
**Description**: Process registration and create tenant
**Content-Type**: `application/x-www-form-urlencoded`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | string | Yes | Unique username (becomes subdomain) |
| `email` | string | Yes | Valid email address |
| `password` | string | Yes | User password |
| `confirm_password` | string | Yes | Password confirmation |

**Example Request**:
```bash
curl -X POST http://127.0.0.1:8000/register/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&email=john@example.com&password=securepass&confirm_password=securepass"
```

**Success Response**:
- **Status**: `302 Found` (Redirect)
- **Location**: `/` (Home page)
- **Message**: "Account created successfully! Your blog is available at john_doe.localhost:8000"

**Error Responses**:
- **Status**: `200 OK` (Form with errors)
- **Messages**: 
  - "All fields are required."
  - "Passwords do not match."
  - "Username already exists."
  - "Email already exists."

### User Login
- **URL**: `/login/`
- **Method**: `GET`, `POST`
- **Description**: User authentication
- **Authentication**: Not required
- **Template**: `accounts/login.html`

#### GET Request
**Description**: Display login form
**Response**: HTML login form

#### POST Request
**Description**: Authenticate user
**Content-Type**: `application/x-www-form-urlencoded`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | string | Yes | Username or email |
| `password` | string | Yes | User password |

**Example Request**:
```bash
curl -X POST http://127.0.0.1:8000/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=securepass"
```

**Success Response**:
- **Status**: `302 Found` (Redirect)
- **Location**: `/` (Home page)
- **Message**: "Welcome back, john_doe!"

**Error Response**:
- **Status**: `200 OK` (Form with errors)
- **Message**: "Invalid username or password."

### User Logout
- **URL**: `/logout/`
- **Method**: `GET`
- **Description**: User logout with redirect to home
- **Authentication**: Required
- **Redirect**: Home page with success message

**Example Request**:
```bash
curl -X GET http://127.0.0.1:8000/logout/ \
  -H "Cookie: sessionid=your_session_id"
```

**Response**:
- **Status**: `302 Found` (Redirect)
- **Location**: `/` (Home page)
- **Message**: "You have been logged out successfully."

---

## 📝 Blog Endpoints (Tenant-Specific)

### Blog Post List
- **URL**: `/blog/`
- **Method**: `GET`
- **Description**: Display all blog posts for the current tenant
- **Authentication**: Required
- **Template**: `accounts/blog/post_list.html`
- **Context**: `{'posts': posts}`

**Example Request**:
```bash
curl -X GET http://username.localhost:8000/blog/ \
  -H "Cookie: sessionid=your_session_id"
```

**Response**: HTML page with:
- List of all blog posts in card format
- Post title, content preview, creation date
- Action buttons (View, Edit, Delete)
- "Create New Post" button

**Empty State**: If no posts exist, shows:
- Empty state message
- "Create Your First Post" button

### Create Blog Post
- **URL**: `/blog/create/`
- **Method**: `GET`, `POST`
- **Description**: Create a new blog post
- **Authentication**: Required
- **Template**: `accounts/blog/post_create.html`

#### GET Request
**Description**: Display post creation form
**Response**: HTML form for creating posts

#### POST Request
**Description**: Process post creation
**Content-Type**: `application/x-www-form-urlencoded`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | string | Yes | Post title (max 255 characters) |
| `content` | string | Yes | Post content |

**Example Request**:
```bash
curl -X POST http://username.localhost:8000/blog/create/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Cookie: sessionid=your_session_id" \
  -d "title=My First Post&content=This is the content of my first blog post."
```

**Success Response**:
- **Status**: `302 Found` (Redirect)
- **Location**: `/blog/` (Post list)
- **Message**: "Post created successfully!"

**Error Response**:
- **Status**: `200 OK` (Form with errors)
- **Message**: "Please fill in all fields."

---

## ⚙️ Admin Endpoints

### Django Admin
- **URL**: `/admin/`
- **Method**: `GET`, `POST`
- **Description**: Django admin interface
- **Authentication**: Required (superuser)
- **Template**: Django admin templates

**Example Request**:
```bash
curl -X GET http://127.0.0.1:8000/admin/ \
  -H "Cookie: sessionid=admin_session_id"
```

**Response**: Django admin interface with:
- User management
- Tenant management
- Domain management
- Blog post management (per tenant)

---

## 🔄 URL Patterns

### Main URLs (`EchoBlogs/urls.py`)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),           # home, login, logout, register
    path('blog/', include('blog.urls')),          # tenant-specific blog posts
]
```

### Account URLs (`accounts/urls.py`)
```python
urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
]
```

### Blog URLs (`blog/urls.py`)
```python
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
]
```

---

## 🌐 Domain-Based Routing

### Public Schema Access
- **Main Domain**: `127.0.0.1:8000` or `localhost:8000`
- **Purpose**: User registration, login, main landing page
- **Schema**: `public`

### Tenant Schema Access
- **Format**: `{username}.localhost:8000`
- **Examples**: 
  - `john.localhost:8000`
  - `jane.localhost:8000`
- **Purpose**: Individual blog management
- **Schema**: `{username}` (tenant-specific)

---

## 📊 Response Formats

### HTML Responses
All endpoints return HTML responses with:
- **Content-Type**: `text/html; charset=utf-8`
- **Template**: Django template rendering
- **Bootstrap**: Modern UI with Bootstrap 5
- **Responsive**: Mobile-friendly design

### Error Responses
Error responses include:
- **Status Codes**: Appropriate HTTP status codes
- **Error Messages**: User-friendly error messages
- **Form Validation**: Field-specific validation errors
- **Flash Messages**: Success/error notifications

---

## 🔐 Authentication Requirements

### Public Endpoints
- **Home Page**: No authentication required
- **Registration**: No authentication required
- **Login**: No authentication required

### Protected Endpoints
- **Logout**: Requires authentication
- **Blog Management**: Requires authentication
- **Admin Interface**: Requires superuser authentication

### Session Management
- **Session Storage**: Database-backed sessions
- **Session Timeout**: Django default (2 weeks)
- **CSRF Protection**: All forms protected with CSRF tokens

---

## 📝 Request Examples

### Complete Registration Flow
```bash
# 1. Visit registration page
curl -X GET http://127.0.0.1:8000/register/

# 2. Submit registration form
curl -X POST http://127.0.0.1:8000/register/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=newuser&email=new@example.com&password=password123&confirm_password=password123"

# 3. Access personal blog (after registration)
curl -X GET http://newuser.localhost:8000/blog/
```

### Complete Login Flow
```bash
# 1. Visit login page
curl -X GET http://127.0.0.1:8000/login/

# 2. Submit login form
curl -X POST http://127.0.0.1:8000/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=existinguser&password=password123"

# 3. Access blog (after login)
curl -X GET http://existinguser.localhost:8000/blog/
```

### Blog Post Creation Flow
```bash
# 1. Visit post creation page
curl -X GET http://username.localhost:8000/blog/create/ \
  -H "Cookie: sessionid=your_session_id"

# 2. Submit post creation form
curl -X POST http://username.localhost:8000/blog/create/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Cookie: sessionid=your_session_id" \
  -d "title=My New Post&content=This is the content of my new blog post."

# 3. View updated post list
curl -X GET http://username.localhost:8000/blog/ \
  -H "Cookie: sessionid=your_session_id"
```

---

## 🚀 Future API Endpoints

### Planned REST API Endpoints
```python
# Authentication API
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
GET  /api/auth/user/

# Blog API
GET    /api/posts/
POST   /api/posts/
GET    /api/posts/{id}/
PUT    /api/posts/{id}/
DELETE /api/posts/{id}/

# Tenant API
GET  /api/tenants/
POST /api/tenants/
GET  /api/tenants/{id}/
PUT  /api/tenants/{id}/
```

---

## 📚 Additional Resources

- [Django URL Patterns](https://docs.djangoproject.com/en/stable/topics/http/urls/)
- [Django Views](https://docs.djangoproject.com/en/stable/topics/http/views/)
- [django-tenants URL Routing](https://django-tenants.readthedocs.io/en/latest/use.html#url-routing)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
