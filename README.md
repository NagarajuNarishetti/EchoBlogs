# 📘 EchoBlogs - Multitenant Blogging Platform

<div align="center">
  <img src="https://img.shields.io/badge/Django-5.2-green.svg" alt="Django Version">
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/PostgreSQL-14+-blue.svg" alt="PostgreSQL Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</div>

## 🚀 Project Overview

EchoBlogs is a **multitenant blog application** that provides complete data isolation for each user. Each tenant (organization/user) gets their own **isolated database schema**, ensuring privacy and security while allowing multiple bloggers to use the same platform.

### ✨ Key Features

- 🔐 **Complete Data Isolation**: Each user gets their own database schema
- 🎨 **Modern UI**: Beautiful, responsive interface with Bootstrap 5
- 👤 **User Authentication**: Complete signup, signin, and logout functionality
- 📝 **Blog Management**: Create, view, and manage blog posts
- 🌐 **Custom Domains**: Each user gets their own subdomain (username.localhost)
- ⚡ **Auto-provisioning**: Automatic tenant and schema creation on registration
- 🛡️ **Security**: CSRF protection, secure password handling, input validation

## 🏗️ Architecture

EchoBlogs uses a **schema-based multitenancy** approach:

- **Public Schema**: Handles user registration, authentication, and tenant management
- **Tenant Schemas**: Each user gets an isolated schema for their blog data
- **Domain Mapping**: Each tenant is accessible via their unique subdomain

## 🛠️ Tech Stack

- **Backend**: Django 5.2+ with django-tenants
- **Database**: PostgreSQL 14+
- **Frontend**: Django Templates + Bootstrap 5
- **Authentication**: Django's built-in auth system
- **Language**: Python 3.12+
- **Icons**: Bootstrap Icons

## 📁 Project Structure

```
EchoBlogs/
├── EchoBlogs/                 # Main Django project
│   ├── settings.py            # Project configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI configuration
├── accounts/                  # Authentication & user management (SHARED)
│   ├── views.py              # Login, logout, registration views
│   ├── urls.py               # Account-related URLs
│   └── models.py             # User models (if any)
├── blog/                     # Blog functionality (TENANT-SPECIFIC)
│   ├── models.py             # Post model
│   ├── views.py              # Blog views
│   └── urls.py               # Blog URLs
├── tenants/                  # Tenant management
│   ├── models.py             # Client & Domain models
│   └── management/           # Custom management commands
├── templates/                # HTML templates
│   ├── base.html             # Base template with Bootstrap
│   ├── home.html             # Landing page
│   └── accounts/             # Authentication templates
├── static/                   # Static files directory
├── requirements.txt          # Python dependencies
└── manage.py                 # Django management script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/EchoBlogs.git
   cd EchoBlogs
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```sql
   CREATE DATABASE echoblogsdb;
   CREATE USER postgres WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE echoblogsdb TO postgres;
   ```

5. **Configure settings**
   Update `EchoBlogs/settings.py` with your database credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django_tenants.postgresql_backend',
           'NAME': 'echoblogsdb',
           'USER': 'postgres',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate_schemas --shared
   ```

7. **Setup public tenant**
   ```bash
   python manage.py setup_public_tenant
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 📖 Documentation

- [API Documentation](docs/API.md) - Complete API reference
- [Architecture Guide](docs/ARCHITECTURE.md) - Detailed architecture explanation
- [Tech Stack](docs/TECH_STACK.md) - Technology choices and rationale
- [Tenant Creation](docs/TENANT_CREATION.md) - How tenant creation works
- [Endpoints](docs/ENDPOINTS.md) - All available endpoints
- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [Contributing](CONTRIBUTING.md) - How to contribute to the project

## 🎯 How It Works

### 1. User Registration
- User visits the main site (127.0.0.1:8000)
- Fills out registration form
- System creates user account in public schema
- New tenant schema is automatically created
- Domain mapping is established (username.localhost)

### 2. Tenant Access
- User can access their blog via their subdomain
- Each tenant has isolated database schema
- Complete data separation between tenants

### 3. Blog Management
- Users create posts in their tenant schema
- Posts are completely isolated from other users
- Modern UI for post creation and management

## 🔧 Configuration

### Environment Variables
Create a `.env` file (optional):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=echoblogsdb
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### Django Settings
Key settings in `EchoBlogs/settings.py`:
- `SHARED_APPS`: Apps that run on public schema
- `TENANT_APPS`: Apps that run on tenant schemas
- `TENANT_MODEL`: Points to Client model
- `TENANT_DOMAIN_MODEL`: Points to Domain model

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure proper database credentials
- [ ] Set up static file serving
- [ ] Configure domain mapping
- [ ] Set up SSL certificates
- [ ] Configure email settings

### Docker Deployment
```bash
# Build image
docker build -t echoblogs .

# Run container
docker run -p 8000:8000 echoblogs
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django team for the amazing framework
- django-tenants for multitenancy support
- Bootstrap team for the UI framework
- All contributors and users

## 📞 Support

- 📧 Email: support@echoblogs.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/EchoBlogs/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/EchoBlogs/discussions)

---

<div align="center">
  <strong>Made with ❤️ for multitenant blogging</strong>
</div>
