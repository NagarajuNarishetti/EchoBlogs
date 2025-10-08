# EchoBlogs REST API Documentation

This document describes the REST API for EchoBlogs and how to verify everything using Postman. Use these APIs today with Postman and later from any frontend (e.g., Next.js).

Base path for all endpoints: `/api/`

Important: EchoBlogs is multitenant. Registration and login happen on the public domain (`localhost`). Blog data (posts) are accessed via each tenant subdomain (`<tenant>.localhost`).

## Authentication

Auth uses JWT (JSON Web Tokens) via SimpleJWT. Obtain tokens with login or register, then send `Authorization: Bearer <access_token>` on protected requests. Refresh tokens with `/auth/refresh/`.

### Register
- Method: POST
- URL: http://localhost:8000/api/auth/register/
- Headers:
  - Content-Type: application/json
- Body (raw JSON):
```json
{ "username": "john", "email": "john@example.com", "password": "secret123" }
```
- Expected 201 Response:
```json
{
  "user": {"id": 1, "username": "john", "email": "john@example.com"},
  "domain": "john.localhost",
  "tokens": {"access": "...", "refresh": "..."}
}
```
- Notes: Creates the user, tenant schema, and primary domain `john.localhost`.

### Login
- Method: POST
- URL: http://localhost:8000/api/auth/login/
- Headers:
  - Content-Type: application/json
- Body (raw JSON):
```json
{ "username": "john", "password": "secret123" }
```
- Expected 200 Response:
```json
{
  "user": {"id": 1, "username": "john", "email": "john@example.com"},
  "tokens": {"access": "...", "refresh": "..."}
}
```
- Notes: Save `tokens.access` → `ACCESS_TOKEN`, `tokens.refresh` → `REFRESH_TOKEN` in Postman env.

### Refresh Token
- Method: POST
- URL: http://localhost:8000/api/auth/refresh/
- Headers:
  - Content-Type: application/json
- Body (raw JSON):
```json
{ "refresh": "<refresh_token>" }
```
- Expected 200 Response:
```json
{ "access": "..." }
```
- Notes: Update your `ACCESS_TOKEN` environment variable with the response value.

### Current User
- Method: GET
- URL: http://localhost:8000/api/auth/me/
- Headers:
  - Authorization: Bearer {{ACCESS_TOKEN}}
- Expected 200 Response:
```json
{ "id": 1, "username": "john", "email": "john@example.com" }
```

## Blog Posts (Tenant-aware)

Posts are automatically tenant-scoped by `django-tenants` using the request host. For local development, call APIs from the tenant subdomain (`http://<username>.localhost:8000`). If you registered the username `john`, you should use `http://john.localhost:8000` for all posts endpoints.

### List Posts
- Method: GET
- URL: http://<tenant>.localhost:8000/api/posts/
- Headers: (none required)
- Expected 200 Response:
```json
[{"id":1,"title":"Hello","content":"...","author":1,"author_username":"john","created_at":"...","updated_at":"...","is_published":true}]
```

### Retrieve Post
- Method: GET
- URL: http://<tenant>.localhost:8000/api/posts/{id}/
- Headers: (none required)

### Create Post
- Method: POST
- URL: http://<tenant>.localhost:8000/api/posts/
- Headers:
  - Authorization: Bearer {{ACCESS_TOKEN}}
  - Content-Type: application/json
- Body (raw JSON):
```json
{ "title": "My first post", "content": "Post content", "is_published": true }
```
-- Expected 201 Response: Created post object

Postman tips:
- URL: `http://{{TENANT}}.localhost:8000/api/posts/` (set `TENANT` to your username)
- Headers: `Content-Type: application/json`, `Authorization: Bearer {{ACCESS_TOKEN}}`

### Update Post
- Method: PUT (or PATCH)
- URL: http://<tenant>.localhost:8000/api/posts/{id}/
- Headers:
  - Authorization: Bearer {{ACCESS_TOKEN}} (must be author)
  - Content-Type: application/json
- Body (raw JSON): any editable fields from the serializer

Postman tips:
- Use either `PUT` (full update) or `PATCH` (partial update)

### Delete Post
- Method: DELETE
- URL: http://<tenant>.localhost:8000/api/posts/{id}/
- Headers:
  - Authorization: Bearer {{ACCESS_TOKEN}} (must be author)
- Expected 204 No Content

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

## 📡 API Reference Notes

This project is API-first. Any references to server-rendered templates or form-based endpoints have been removed in favor of JSON over HTTP endpoints under `/api/`. Use JWT in the `Authorization` header and tenant subdomains for tenant-scoped resources.
