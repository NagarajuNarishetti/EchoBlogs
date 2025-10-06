# 📡 API Documentation

## Overview

EchoBlogs currently uses Django's traditional view-based architecture with HTML templates. This document outlines the current endpoints and provides guidance for future API development.

## 🔗 Current Endpoints

### Authentication Endpoints

#### Home Page
- **URL**: `/`
- **Method**: `GET`
- **Description**: Landing page with feature highlights and call-to-action buttons
- **Template**: `home.html`
- **Authentication**: Not required

#### User Registration
- **URL**: `/register/`
- **Method**: `GET`, `POST`
- **Description**: User registration with automatic tenant creation
- **Template**: `accounts/register.html`
- **Authentication**: Not required
- **POST Data**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "confirm_password": "string"
  }
  ```

#### User Login
- **URL**: `/login/`
- **Method**: `GET`, `POST`
- **Description**: User authentication
- **Template**: `accounts/login.html`
- **Authentication**: Not required
- **POST Data**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

#### User Logout
- **URL**: `/logout/`
- **Method**: `GET`
- **Description**: User logout with redirect to home
- **Authentication**: Required
- **Redirect**: Home page with success message

### Blog Endpoints (Tenant-Specific)

#### Blog Post List
- **URL**: `/blog/`
- **Method**: `GET`
- **Description**: Display all blog posts for the current tenant
- **Template**: `accounts/blog/post_list.html`
- **Authentication**: Required
- **Context**: `{'posts': posts}`

#### Create Blog Post
- **URL**: `/blog/create/`
- **Method**: `GET`, `POST`
- **Description**: Create a new blog post
- **Template**: `accounts/blog/post_create.html`
- **Authentication**: Required
- **POST Data**:
  ```json
  {
    "title": "string",
    "content": "string"
  }
  ```

### Admin Endpoints

#### Django Admin
- **URL**: `/admin/`
- **Method**: `GET`, `POST`
- **Description**: Django admin interface
- **Authentication**: Required (superuser)

## 🚀 Future API Development

### REST API with Django REST Framework

When implementing a REST API, consider these endpoints:

#### Authentication API
```python
# Authentication endpoints
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/refresh/
GET  /api/auth/user/
PUT  /api/auth/user/
```

#### Blog API
```python
# Blog endpoints
GET    /api/posts/
POST   /api/posts/
GET    /api/posts/{id}/
PUT    /api/posts/{id}/
DELETE /api/posts/{id}/
GET    /api/posts/{id}/comments/
POST   /api/posts/{id}/comments/
```

#### Tenant API
```python
# Tenant management
GET  /api/tenants/
POST /api/tenants/
GET  /api/tenants/{id}/
PUT  /api/tenants/{id}/
DELETE /api/tenants/{id}/
```

### API Response Format

#### Success Response
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Sample Post",
    "content": "Post content...",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "author": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    }
  },
  "message": "Post created successfully"
}
```

#### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "title": ["This field is required."],
      "content": ["This field is required."]
    }
  }
}
```

### HTTP Status Codes

- `200 OK` - Successful GET, PUT requests
- `201 Created` - Successful POST requests
- `204 No Content` - Successful DELETE requests
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## 🔐 Authentication

### Current Authentication
- Django's built-in session-based authentication
- CSRF protection on all forms
- Secure password handling

### Future API Authentication
Consider implementing:
- JWT (JSON Web Tokens)
- OAuth 2.0
- API Key authentication
- Rate limiting

## 📝 Request/Response Examples

### Register User
```bash
curl -X POST http://127.0.0.1:8000/register/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&email=john@example.com&password=securepass&confirm_password=securepass"
```

### Create Blog Post
```bash
curl -X POST http://127.0.0.1:8000/blog/create/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "title=My First Post&content=This is my first blog post content"
```

## 🛡️ Security Considerations

### Current Security Features
- CSRF protection
- SQL injection prevention (Django ORM)
- XSS protection (template auto-escaping)
- Secure password hashing
- Session security

### Future API Security
- Input validation and sanitization
- Rate limiting
- API versioning
- CORS configuration
- Content Security Policy (CSP)

## 📊 Rate Limiting

### Current Implementation
- No rate limiting implemented

### Recommended Rate Limits
- Authentication endpoints: 5 requests/minute
- Blog creation: 10 requests/hour
- General API: 100 requests/hour

## 🔄 API Versioning

### Current Version
- No API versioning (template-based)

### Future Versioning Strategy
- URL-based versioning: `/api/v1/`, `/api/v2/`
- Header-based versioning: `Accept: application/vnd.echoblogs.v1+json`
- Query parameter versioning: `?version=1`

## 📈 Monitoring and Analytics

### Recommended Metrics
- Request count per endpoint
- Response time percentiles
- Error rate by endpoint
- User authentication success rate
- Tenant creation rate

### Logging
- Request/response logging
- Error logging
- Security event logging
- Performance metrics

## 🧪 Testing

### API Testing Tools
- Postman
- Insomnia
- curl
- pytest-django
- Django REST framework test utilities

### Test Coverage
- Unit tests for views
- Integration tests for API endpoints
- Authentication tests
- Permission tests
- Error handling tests

## 📚 Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Django Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)
- [REST API Design Best Practices](https://restfulapi.net/)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)
