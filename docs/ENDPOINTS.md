# 🔗 Endpoints Documentation

## Overview

This document provides a comprehensive list of all available endpoints in EchoBlogs, including their methods, parameters, responses, and usage examples.

## 🌐 Base URLs

- **Development**: `http://127.0.0.1:8000`
- **Production**: `https://yourdomain.com`
- **Tenant Access**: `http://username.localhost:8000` (for tenant-specific endpoints)

## 📋 Endpoint Categories (API-first)

- **Auth (public domain)**: `/api/auth/*`
- **Posts (tenant domain)**: `/api/posts/*`
- **Admin**: `/admin/` (Django admin)

---

## 🧭 Base URLs

- **Public**: `http://localhost:8000`
- **Tenant**: `http://<username>.localhost:8000`

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

## 🔐 Authentication Endpoints (JSON)

### Register
- **URL**: `/api/auth/register/`
- **Method**: `POST`
- **Body**:
```json
{ "username": "string", "email": "string", "password": "string" }
```
- **Response**: 201 with `{ user, domain, tokens }`

### Login
- **URL**: `/api/auth/login/`
- **Method**: `POST`
- **Body**:
```json
{ "username": "string", "password": "string" }
```
- **Response**: 200 with `{ user, tokens }`

### Refresh
- **URL**: `/api/auth/refresh/`
- **Method**: `POST`
- **Body**:
```json
{ "refresh": "token" }
```

### Me
- **URL**: `/api/auth/me/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <access>`

> Note: Admin uses Django's session-based auth; API endpoints use JWT.

---

## 📝 Blog Endpoints (Tenant-Specific, JSON)

### List Posts
- **URL**: `/api/posts/`
- **Method**: `GET`
- **Response**: 200 JSON array

### Create Post
- **URL**: `/api/posts/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <access>`, `Content-Type: application/json`
- **Body**:
```json
{ "title": "string", "content": "string", "is_published": true }
```
- **Response**: 201 with post JSON

### Retrieve Post
- **URL**: `/api/posts/{id}/`
- **Method**: `GET`

### Update Post
- **URL**: `/api/posts/{id}/`
- **Method**: `PATCH` or `PUT`
- **Headers**: `Authorization: Bearer <access>`, `Content-Type: application/json`

### Delete Post
- **URL**: `/api/posts/{id}/`
- **Method**: `DELETE`
- **Headers**: `Authorization: Bearer <access>`

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

## 🔄 URL Patterns (High-level)

- Public domain routes expose `/api/auth/*`
- Tenant domain routes expose `/api/posts/*`
- Django admin remains at `/admin/`

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

### JSON Responses
All API endpoints return JSON with appropriate HTTP status codes.

### Error Responses
Error responses include:
- **Status Codes**: Appropriate HTTP status codes
- **Error Messages**: User-friendly error messages
- **Form Validation**: Field-specific validation errors
- **Flash Messages**: Success/error notifications

---

## 🔐 Authentication Requirements

- Send `Authorization: Bearer <access>` for protected endpoints
- Obtain tokens from `/api/auth/login/` or `/api/auth/register/`

---

## 📝 Request Examples

### Registration/Login (cURL)
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","email":"new@example.com","password":"password123"}'

curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"password123"}'
```

### Posts (cURL)
```bash
curl -X POST http://newuser.localhost:8000/api/posts/ \
  -H "Authorization: Bearer <ACCESS>" \
  -H "Content-Type: application/json" \
  -d '{"title":"My New Post","content":"This is the content of my new blog post."}'

curl -X GET http://newuser.localhost:8000/api/posts/
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
