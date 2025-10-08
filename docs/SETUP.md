# 🚀 Setup Guide

## Overview

This comprehensive setup guide will walk you through installing, configuring, and running EchoBlogs on your local machine or production environment.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.12 or higher
- **PostgreSQL**: 14 or higher
- **Git**: For version control
- **Memory**: Minimum 4GB RAM
- **Storage**: At least 2GB free space

### Software Installation

#### 1. Python Installation
**Windows**:
```bash
# Download from python.org or use chocolatey
choco install python

# Verify installation
python --version
```

**macOS**:
```bash
# Using Homebrew
brew install python

# Verify installation
python3 --version
```

**Linux (Ubuntu/Debian)**:
```bash
# Update package list
sudo apt update

# Install Python
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
```

#### 2. PostgreSQL Installation
**Windows**:
```bash
# Download from postgresql.org or use chocolatey
choco install postgresql

# Start PostgreSQL service
net start postgresql-x64-14
```

**macOS**:
```bash
# Using Homebrew
brew install postgresql

# Start PostgreSQL service
brew services start postgresql
```

**Linux (Ubuntu/Debian)**:
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### 3. Git Installation
**Windows**:
```bash
# Download from git-scm.com or use chocolatey
choco install git
```

**macOS**:
```bash
# Using Homebrew
brew install git
```

**Linux (Ubuntu/Debian)**:
```bash
# Install Git
sudo apt install git
```

## 🔧 Development Setup

### 1. Clone Repository
```bash
# Clone the repository
git clone https://github.com/yourusername/EchoBlogs.git
cd EchoBlogs
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Optional: Install development dependencies
pip install pytest pytest-django coverage black flake8
```

### 4. Database Setup

#### Create Database
```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database
CREATE DATABASE echoblogsdb;

-- Create user (optional, can use existing postgres user)
CREATE USER echoblogs_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE echoblogsdb TO echoblogs_user;

-- Exit psql
\q
```

#### Configure Database Settings
Update `EchoBlogs/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'echoblogsdb',
        'USER': 'echoblogs_user',  # or 'postgres'
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Environment Configuration

#### Create Environment File (Optional)
Create `.env` file in project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=echoblogsdb
DATABASE_USER=echoblogs_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

#### Update Settings for Environment Variables
```python
# EchoBlogs/settings.py
import os
from decouple import config  # pip install python-decouple

SECRET_KEY = config('SECRET_KEY', default='replace-this-with-your-own-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': config('DATABASE_NAME', default='echoblogsdb'),
        'USER': config('DATABASE_USER', default='postgres'),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}
```

### 6. Run Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations to shared schema
python manage.py migrate_schemas --shared
```

### 7. Setup Public Tenant
```bash
# Create public tenant for main domain
python manage.py setup_public_tenant
```

### 8. Create Superuser (Optional)
```bash
# Create admin user
python manage.py createsuperuser

# Follow prompts to create admin account
```

### 9. Start Development Server
```bash
# Start Django development server
python manage.py runserver

# Server will start on http://127.0.0.1:8000/
```

## 🌐 Access the Application

### Main Site
- **URL**: http://127.0.0.1:8000/
- **Purpose**: Landing page, registration, login

### Admin Interface
- **URL**: http://127.0.0.1:8000/admin/
- **Purpose**: Django admin for managing tenants and users

### User Blogs
- **URL**: http://username.localhost:8000/
- **Purpose**: Individual user blogs (after registration)

### API and Postman Quick Test
- Register on public domain: `POST http://localhost:8000/api/auth/register/`
- Login on public domain: `POST http://localhost:8000/api/auth/login/`
- Use tenant domain for posts: `GET http://<username>.localhost:8000/api/posts/`
- See `docs/API.md` for full Postman instructions and environment variables

## 🐳 Docker Setup (Alternative)

### 1. Create Dockerfile
```dockerfile
# Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 2. Create docker-compose.yml
```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: echoblogsdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DEBUG=True
      - DATABASE_HOST=db
      - DATABASE_NAME=echoblogsdb
      - DATABASE_USER=postgres
      - DATABASE_PASSWORD=postgres

volumes:
  postgres_data:
```

### 3. Run with Docker
```bash
# Build and start containers
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate_schemas --shared

# Setup public tenant
docker-compose exec web python manage.py setup_public_tenant

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## 🚀 Production Setup

### 1. Production Environment Variables
```env
# .env.production
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_NAME=echoblogsdb
DATABASE_USER=echoblogs_user
DATABASE_PASSWORD=your-secure-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 2. Install Production Dependencies
```bash
# Install production WSGI server
pip install gunicorn

# Install reverse proxy (if not using Docker)
sudo apt install nginx
```

### 3. Configure Static Files
```python
# EchoBlogs/settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Collect static files
python manage.py collectstatic
```

### 4. Configure Nginx
```nginx
# /etc/nginx/sites-available/echoblogs
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /path/to/EchoBlogs/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Configure Gunicorn
```bash
# Create gunicorn configuration
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

### 6. Start Production Server
```bash
# Start with Gunicorn
gunicorn --config gunicorn.conf.py EchoBlogs.wsgi:application

# Or use systemd service
sudo systemctl start echoblogs
sudo systemctl enable echoblogs
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Database Connection Error
**Error**: `django.db.utils.OperationalError: could not connect to server`
**Solutions**:
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify database credentials in settings.py
- Check firewall settings
- Ensure database exists

#### 2. Migration Errors
**Error**: `django.db.utils.ProgrammingError: relation does not exist`
**Solutions**:
- Run migrations: `python manage.py migrate_schemas --shared`
- Check database permissions
- Verify database connection

#### 3. "No tenant for hostname" Error
**Error**: `No tenant for hostname '127.0.0.1'`
**Solutions**:
- Run: `python manage.py setup_public_tenant`
- Check Domain table in database
- Verify public tenant exists

#### 4. Static Files Not Loading
**Error**: CSS/JS files not loading
**Solutions**:
- Run: `python manage.py collectstatic`
- Check STATIC_URL and STATIC_ROOT settings
- Verify static files directory exists

#### 5. Permission Denied Errors
**Error**: `Permission denied` on file operations
**Solutions**:
- Check file permissions: `chmod 755 /path/to/files`
- Verify user has write permissions
- Check SELinux settings (Linux)

### Debug Commands
```bash
# Check Django configuration
python manage.py check

# Check database connection
python manage.py dbshell

# List all migrations
python manage.py showmigrations

# Check tenant schemas
python manage.py shell
>>> from tenants.models import Client
>>> Client.objects.all()

# Check domain mappings
>>> from tenants.models import Domain
>>> Domain.objects.all()
```

## 📊 Performance Optimization

### 1. Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_posts_created_at ON blog_post(created_at);
CREATE INDEX idx_posts_author ON blog_post(author_id);
CREATE INDEX idx_domain_domain ON tenants_domain(domain);
```

### 2. Caching Setup (Future)
```python
# EchoBlogs/settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 3. Static File Optimization
```bash
# Compress static files
pip install django-compressor

# Add to INSTALLED_APPS
COMPRESS_ENABLED = True
```

## 🔒 Security Configuration

### 1. Production Security Settings
```python
# EchoBlogs/settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 2. SSL Configuration
```nginx
# Nginx SSL configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
}
```

## 📈 Monitoring Setup

### 1. Logging Configuration
```python
# EchoBlogs/settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 2. Health Check Endpoint
```python
# accounts/views.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy', 'timestamp': timezone.now()})
```

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
