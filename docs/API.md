# EchoBlogs REST API Documentation

This document describes the REST API for EchoBlogs and how to verify everything using Postman. Use these APIs today with Postman and later from any frontend (e.g., Next.js).

Base path for all endpoints: `/api/`

Important: EchoBlogs is multitenant. Registration and login happen on the public domain (`localhost`). Blog data (posts) are accessed via each tenant subdomain (`<tenant>.localhost`).

## Authentication

Auth uses JWT (JSON Web Tokens) via SimpleJWT. Obtain tokens with login or register, then send `Authorization: Bearer <access_token>` on protected requests. Refresh tokens with `/auth/refresh/`.

### Register
- URL: `POST /api/auth/register/`
- Body (JSON):
```json
{ "username": "john", "email": "john@example.com", "password": "secret123" }
```
- Creates user, tenant schema, and primary domain `john.localhost`.
- Response 201:
```json
{
  "user": {"id": 1, "username": "john", "email": "john@example.com"},
  "domain": "john.localhost",
  "tokens": {"access": "...", "refresh": "..."}
}
```

Postman tips:
- Set request: Method `POST`, URL `http://localhost:8000/api/auth/register/`
- Headers: `Content-Type: application/json`
- Body: raw JSON as above
- Save `tokens.access` in a Postman environment variable (e.g., `ACCESS_TOKEN`)

### Login
- URL: `POST /api/auth/login/`
- Body (JSON):
```json
{ "username": "john", "password": "secret123" }
```
- Response 200:
```json
{
  "user": {"id": 1, "username": "john", "email": "john@example.com"},
  "tokens": {"access": "...", "refresh": "..."}
}
```

Postman tips:
- URL: `http://localhost:8000/api/auth/login/`
- Save `tokens.access` to `ACCESS_TOKEN` and `tokens.refresh` to `REFRESH_TOKEN` in your Postman environment for later use

### Refresh Token
- URL: `POST /api/auth/refresh/`
- Body (JSON):
```json
{ "refresh": "<refresh_token>" }
```
- Response 200: `{ "access": "..." }`

Postman tips:
- URL: `http://localhost:8000/api/auth/refresh/`
- Update your `ACCESS_TOKEN` variable with the new token

### Current User
- URL: `GET /api/auth/me/`
- Headers: `Authorization: Bearer <access_token>`
- Response 200: `{ "id": 1, "username": "john", "email": "john@example.com" }`

Postman tips:
- Add header: `Authorization: Bearer {{ACCESS_TOKEN}}`

## Blog Posts (Tenant-aware)

Posts are automatically tenant-scoped by `django-tenants` using the request host. For local development, call APIs from the tenant subdomain (`http://<username>.localhost:8000`). If you registered the username `john`, you should use `http://john.localhost:8000` for all posts endpoints.

### List Posts
- URL: `GET http://<tenant>.localhost:8000/api/posts/`
- Public: yes
- Response 200:
```json
[{"id":1,"title":"Hello","content":"...","author":1,"author_username":"john","created_at":"...","updated_at":"...","is_published":true}]
```

### Retrieve Post
- URL: `GET http://<tenant>.localhost:8000/api/posts/{id}/`
- Public: yes

### Create Post
- URL: `POST http://<tenant>.localhost:8000/api/posts/`
- Headers: `Authorization: Bearer <access_token>`
- Body (JSON):
```json
{ "title": "My first post", "content": "Post content", "is_published": true }
```
- Response 201: Created post object

Postman tips:
- URL: `http://{{TENANT}}.localhost:8000/api/posts/` (set Postman variable `TENANT` to your username)
- Headers: `Content-Type: application/json`, `Authorization: Bearer {{ACCESS_TOKEN}}`

### Update Post
- URL: `PUT http://<tenant>.localhost:8000/api/posts/{id}/`
- Headers: `Authorization: Bearer <access_token>` (must be author)
- Body (JSON): any editable fields from the serializer

Postman tips:
- Use either `PUT` (full update) or `PATCH` (partial update)

### Delete Post
- URL: `DELETE http://<tenant>.localhost:8000/api/posts/{id}/`
- Headers: `Authorization: Bearer <access_token>` (must be author)

Postman tips:
- The endpoint returns 204 No Content on success

## Quick Start (cURL)

```bash
# 1) Register (public domain)
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"secret123"}'

# 2) Login (public domain) -> get access token
ACCESS=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}' | python -c "import sys, json; print(json.load(sys.stdin)['tokens']['access'])")

# 3) Create a post on tenant domain
curl -X POST http://john.localhost:8000/api/posts/ \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"World"}'

# 4) List posts (tenant domain)
curl http://john.localhost:8000/api/posts/
```

## Postman Collection Setup

You can create a Postman Collection with these variables for convenience:

- `BASE_PUBLIC_URL`: `http://localhost:8000`
- `TENANT`: your username, e.g., `john`
- `BASE_TENANT_URL`: `http://{{TENANT}}.localhost:8000`
- `ACCESS_TOKEN`: set after login/register
- `REFRESH_TOKEN`: set after login/register

Then define these requests in the collection:

1) Register
- Method: POST
- URL: `{{BASE_PUBLIC_URL}}/api/auth/register/`
- Headers: `Content-Type: application/json`
- Body (raw JSON): `{ "username": "{{TENANT}}", "email": "john@example.com", "password": "secret123" }`

2) Login
- Method: POST
- URL: `{{BASE_PUBLIC_URL}}/api/auth/login/`
- Body (raw JSON): `{ "username": "{{TENANT}}", "password": "secret123" }`
- Test script (Postman):
```javascript
let json = pm.response.json();
pm.environment.set("ACCESS_TOKEN", json.tokens.access);
pm.environment.set("REFRESH_TOKEN", json.tokens.refresh);
```

3) Me
- Method: GET
- URL: `{{BASE_PUBLIC_URL}}/api/auth/me/`
- Headers: `Authorization: Bearer {{ACCESS_TOKEN}}`

4) Create Post
- Method: POST
- URL: `{{BASE_TENANT_URL}}/api/posts/`
- Headers: `Authorization: Bearer {{ACCESS_TOKEN}}`, `Content-Type: application/json`
- Body: `{ "title": "My first post", "content": "Post content" }`

5) List Posts
- Method: GET
- URL: `{{BASE_TENANT_URL}}/api/posts/`

6) Retrieve Post
- Method: GET
- URL: `{{BASE_TENANT_URL}}/api/posts/:id/`

7) Update Post
- Method: PATCH
- URL: `{{BASE_TENANT_URL}}/api/posts/:id/`
- Headers: `Authorization: Bearer {{ACCESS_TOKEN}}`, `Content-Type: application/json`
- Body: `{ "title": "Updated" }`

8) Delete Post
- Method: DELETE
- URL: `{{BASE_TENANT_URL}}/api/posts/:id/`
- Headers: `Authorization: Bearer {{ACCESS_TOKEN}}`

## Notes
- Registration must happen on the public domain (`localhost`).
- All tenant data access (posts) should be done via the tenant subdomain (`<username>.localhost`).
- JWT access tokens go in the `Authorization` header as `Bearer <token>`.

## Troubleshooting Postman

- If posts endpoints 404 on `localhost`, you are likely not using the tenant subdomain. Switch to `http://<tenant>.localhost:8000`.
- If you receive 401 Unauthorized on protected endpoints, ensure you are sending `Authorization: Bearer {{ACCESS_TOKEN}}` with a valid (unexpired) token.
- If registration fails with "Registration must be done on public schema.", make sure the request is to `http://localhost:8000` (not a tenant subdomain).

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
