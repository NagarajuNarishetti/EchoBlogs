# EchoBlogs API Testing Guide with Postman

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Understanding Multi-Tenant Architecture](#understanding-multi-tenant-architecture)
4. [API Endpoints](#api-endpoints)
5. [Postman Collection Setup](#postman-collection-setup)
6. [Testing Workflows](#testing-workflows)
7. [Common Issues & Solutions](#common-issues--solutions)

---

## Project Overview

**EchoBlogs** is a Django multi-tenant blog application that allows users to:
- Register and create their own tenant (blog space)
- Login/logout
- Create and view blog posts within their tenant
- Each user gets their own subdomain (e.g., `username.localhost:8000`)

**Tech Stack:**
- Django 5.2+
- django-tenants (multi-tenancy)
- PostgreSQL database
- Session-based authentication

---

## Setup Instructions

### 1. Start Your Django Server
```bash
cd EchoBlogs
python manage.py runserver 0.0.0.0:8000
```

### 2. Database Setup (if not already done)
```bash
python manage.py migrate_schemas --shared
python manage.py migrate_schemas
```

### 3. Create Superuser (optional)
```bash
python manage.py createsuperuser
```

---

## Understanding Multi-Tenant Architecture

Your EchoBlogs project uses **django-tenants** which creates separate database schemas for each user:

- **Public Schema**: Contains user accounts, tenant information
- **Tenant Schemas**: Each user gets their own schema for blog posts

**Domain Structure:**
- Main site: `localhost:8000` (public schema)
- User blogs: `username.localhost:8000` (tenant schema)

---

## API Endpoints

### Base URLs
- **Public Schema**: `http://localhost:8000`
- **Tenant Schema**: `http://username.localhost:8000` (replace `username` with actual username)

### 1. Authentication Endpoints (Public Schema)

#### 1.1 Home Page
- **URL**: `GET http://localhost:8000/`
- **Description**: Main landing page
- **Authentication**: None required

#### 1.2 User Registration
- **URL**: `POST http://localhost:8000/register/`
- **Description**: Create new user account and tenant
- **Content-Type**: `application/x-www-form-urlencoded`

**Request Body:**
```
username: your_username
email: your_email@example.com
password: your_password
confirm_password: your_password
```

**Success Response**: Redirects to home page
**Error Response**: Returns registration form with error messages

#### 1.3 User Login
- **URL**: `POST http://localhost:8000/login/`
- **Description**: Authenticate user
- **Content-Type**: `application/x-www-form-urlencoded`

**Request Body:**
```
username: your_username
password: your_password
```

**Success Response**: Redirects to home page
**Error Response**: Returns login form with error message

#### 1.4 User Logout
- **URL**: `GET http://localhost:8000/logout/`
- **Description**: Logout current user
- **Authentication**: Session required

### 2. Blog Endpoints (Tenant Schema)

#### 2.1 List Blog Posts
- **URL**: `GET http://username.localhost:8000/blog/`
- **Description**: View all published blog posts for the tenant
- **Authentication**: None required (public posts)

#### 2.2 Create Blog Post
- **URL**: `POST http://username.localhost:8000/blog/create/`
- **Description**: Create new blog post
- **Authentication**: Login required
- **Content-Type**: `application/x-www-form-urlencoded`

**Request Body:**
```
title: Your Post Title
content: Your post content here...
```

**Success Response**: Redirects to post list
**Error Response**: Returns create form with error message

### 3. Admin Endpoints

#### 3.1 Django Admin
- **URL**: `GET http://localhost:8000/admin/`
- **Description**: Django admin interface
- **Authentication**: Superuser required

---

## Postman Collection Setup

### Step 1: Create New Collection
1. Open Postman
2. Click "New" → "Collection"
3. Name it "EchoBlogs API"
4. Add description: "Testing EchoBlogs multi-tenant blog application"

### Step 2: Environment Variables
Create environment variables for easy testing:

1. Click "Environments" → "Create Environment"
2. Name: "EchoBlogs Local"
3. Add these variables:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `http://localhost:8000` | `http://localhost:8000` |
| `tenant_url` | `http://{{username}}.localhost:8000` | `http://{{username}}.localhost:8000` |
| `username` | `testuser` | `testuser` |
| `email` | `test@example.com` | `test@example.com` |
| `password` | `testpass123` | `testpass123` |

### Step 3: Create Request Folders
Organize your requests in folders:
- **Authentication** (Public Schema)
- **Blog Management** (Tenant Schema)
- **Admin**

---

## Testing Workflows

### Workflow 1: Complete User Registration and Blog Creation

#### Step 1: Register New User
1. **Request**: `POST {{base_url}}/register/`
2. **Headers**: 
   ```
   Content-Type: application/x-www-form-urlencoded
   ```
3. **Body** (x-www-form-urlencoded):
   ```
   username: {{username}}
   email: {{email}}
   password: {{password}}
   confirm_password: {{password}}
   ```
4. **Expected**: 302 Redirect to home page

#### Step 2: Login User
1. **Request**: `POST {{base_url}}/login/`
2. **Headers**: 
   ```
   Content-Type: application/x-www-form-urlencoded
   ```
3. **Body** (x-www-form-urlencoded):
   ```
   username: {{username}}
   password: {{password}}
   ```
4. **Expected**: 302 Redirect to home page

#### Step 3: View Blog Posts (Tenant Schema)
1. **Request**: `GET {{tenant_url}}/blog/`
2. **Expected**: 200 OK with blog post list

#### Step 4: Create Blog Post (Tenant Schema)
1. **Request**: `POST {{tenant_url}}/blog/create/`
2. **Headers**: 
   ```
   Content-Type: application/x-www-form-urlencoded
   ```
3. **Body** (x-www-form-urlencoded):
   ```
   title: My First Post
   content: This is my first blog post content!
   ```
4. **Expected**: 302 Redirect to blog list

#### Step 5: Verify Post Creation
1. **Request**: `GET {{tenant_url}}/blog/`
2. **Expected**: 200 OK with your new post visible

### Workflow 2: Testing Multi-Tenancy

#### Step 1: Create Second User
1. Update environment variables:
   ```
   username: testuser2
   email: test2@example.com
   ```
2. Register second user using same registration endpoint
3. Login second user

#### Step 2: Verify Tenant Isolation
1. **Request**: `GET http://testuser2.localhost:8000/blog/`
2. **Expected**: Empty blog list (different from first user's posts)

#### Step 3: Create Post for Second User
1. **Request**: `POST http://testuser2.localhost:8000/blog/create/`
2. **Body**: Different post content
3. **Expected**: Post created successfully

#### Step 4: Verify Isolation
1. Check `http://testuser.localhost:8000/blog/` - should only show first user's posts
2. Check `http://testuser2.localhost:8000/blog/` - should only show second user's posts

---

## Postman Request Examples

### 1. User Registration Request
```http
POST http://localhost:8000/register/
Content-Type: application/x-www-form-urlencoded

username=john_doe&email=john@example.com&password=securepass123&confirm_password=securepass123
```

### 2. User Login Request
```http
POST http://localhost:8000/login/
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=securepass123
```

### 3. Create Blog Post Request
```http
POST http://john_doe.localhost:8000/blog/create/
Content-Type: application/x-www-form-urlencoded

title=Welcome to My Blog&content=This is my first blog post. I'm excited to share my thoughts with the world!
```

### 4. View Blog Posts Request
```http
GET http://john_doe.localhost:8000/blog/
```

---

## Postman Settings & Configuration

### 1. Request Settings
- **Follow Redirects**: Enable (Settings → General → "Automatically follow redirects")
- **SSL Certificate Verification**: Disable for localhost testing
- **Send cookies**: Enable for session management

### 2. Headers Configuration
For form submissions, always include:
```
Content-Type: application/x-www-form-urlencoded
```

### 3. Cookie Management
- Enable "Send cookies automatically" in Postman settings
- Django uses session cookies for authentication
- Cookies are domain-specific (localhost vs username.localhost)

### 4. Environment Switching
- Use the environment dropdown to switch between different user configurations
- Create multiple environments for testing different users

---

## Common Issues & Solutions

### Issue 1: "Connection Refused"
**Problem**: Cannot connect to localhost:8000
**Solution**: 
- Ensure Django server is running: `python manage.py runserver 0.0.0.0:8000`
- Check if port 8000 is available

### Issue 2: "Tenant Not Found"
**Problem**: Getting errors when accessing tenant URLs
**Solution**:
- Ensure user is registered first (creates tenant automatically)
- Check if domain exists in database
- Verify tenant schema was created

### Issue 3: "CSRF Token Missing"
**Problem**: Getting CSRF errors on POST requests
**Solution**:
- Django CSRF protection is enabled
- For API testing, you may need to disable CSRF for specific views
- Or include CSRF token in requests (more complex)

### Issue 4: "Authentication Required"
**Problem**: Cannot create blog posts
**Solution**:
- Ensure user is logged in first
- Check session cookies are being sent
- Verify login was successful

### Issue 5: "Schema Does Not Exist"
**Problem**: Database schema errors
**Solution**:
- Run migrations: `python manage.py migrate_schemas`
- Check if tenant was created properly during registration

---

## Advanced Testing Scenarios

### 1. Testing Error Handling
- Try registering with existing username
- Try logging in with wrong password
- Try creating post without title/content
- Try accessing non-existent tenant

### 2. Testing Session Management
- Login user
- Make requests without explicit authentication
- Test logout functionality
- Verify session persistence

### 3. Testing Multi-Tenant Isolation
- Create multiple users
- Verify data isolation between tenants
- Test cross-tenant access attempts

### 4. Performance Testing
- Create multiple blog posts
- Test pagination (if implemented)
- Monitor response times

---

## Data Flow Understanding

### Registration Flow:
1. User submits registration form → `POST /register/`
2. Django creates User in public schema
3. Django creates Client (tenant) with schema_name = username
4. Django creates Domain pointing to username.localhost
5. Django runs migrations for new tenant schema
6. User is auto-logged in and redirected

### Blog Post Creation Flow:
1. User accesses tenant URL → `username.localhost:8000`
2. Django tenant middleware routes to correct schema
3. User creates post → `POST /blog/create/`
4. Post is saved in tenant-specific schema
5. Post appears only in that tenant's blog

### Authentication Flow:
1. User logs in → `POST /login/`
2. Django creates session cookie
3. Cookie is sent with subsequent requests
4. Django middleware validates session
5. User can access protected resources

---

## Tips for Learning Postman

1. **Start Simple**: Begin with GET requests to understand the flow
2. **Use Collections**: Organize requests logically
3. **Environment Variables**: Use variables for easy testing
4. **Test Scripts**: Add JavaScript tests to verify responses
5. **Documentation**: Add descriptions to requests and collections
6. **Export/Import**: Share collections with team members

---

## Next Steps

1. **API Documentation**: Consider adding Django REST Framework for proper API endpoints
2. **Authentication**: Implement token-based authentication for better API testing
3. **Error Handling**: Add proper error responses for API calls
4. **Testing**: Add automated tests using Postman's test runner
5. **Monitoring**: Use Postman monitoring for API health checks

---

This guide should help you understand your EchoBlogs project structure and test all functionality using Postman. Start with the basic workflows and gradually explore more advanced scenarios as you become comfortable with both the project and Postman.
