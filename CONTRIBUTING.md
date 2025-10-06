# 🤝 Contributing Guidelines

## Welcome Contributors!

Thank you for your interest in contributing to EchoBlogs! This document provides guidelines and information for contributors to help maintain code quality and project consistency.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## 📜 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Age, body size, disability, ethnicity
- Gender identity and expression
- Level of experience, nationality
- Personal appearance, race, religion
- Sexual identity and orientation

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior
- Harassment, trolling, insulting comments
- Public or private harassment
- Publishing private information without permission
- Other unprofessional conduct

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL 14+
- Git
- Basic knowledge of Django and multitenancy concepts

### Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/yourusername/EchoBlogs.git
cd EchoBlogs

# Add upstream remote
git remote add upstream https://github.com/originalowner/EchoBlogs.git
```

### Development Environment Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-django coverage black flake8

# Setup database (see SETUP.md for details)
# Run migrations
python manage.py migrate_schemas --shared

# Setup public tenant
python manage.py setup_public_tenant

# Start development server
python manage.py runserver
```

## 🔄 Development Workflow

### Branch Naming Convention
Use descriptive branch names:
- `feature/user-profile-management`
- `bugfix/login-validation-error`
- `hotfix/security-patch`
- `docs/api-documentation-update`

### Commit Message Format
Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(auth): add password reset functionality

fix(blog): resolve post creation validation error

docs(api): update endpoint documentation

test(tenants): add tenant creation tests
```

### Workflow Steps
1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following coding standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Test Your Changes**
   ```bash
   # Run tests
   python manage.py test
   
   # Run with coverage
   coverage run --source='.' manage.py test
   coverage report
   
   # Check code style
   black --check .
   flake8 .
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat(scope): your commit message"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create Pull Request on GitHub
   ```

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Use Flake8 for linting
- Maximum line length: 88 characters (Black default)

### Django Best Practices
- Use Django's built-in features when possible
- Follow Django's naming conventions
- Use Django's ORM instead of raw SQL
- Implement proper error handling

### Code Organization
```python
# File structure example
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Imports: standard library, third-party, local
import os
from datetime import date

from django.contrib.auth import authenticate, login
from django.db import connection

from .models import Post
from .forms import PostForm
```

### Function and Class Documentation
```python
def create_tenant(user_data):
    """
    Create a new tenant with the provided user data.
    
    Args:
        user_data (dict): Dictionary containing user information
            - username (str): Unique username
            - email (str): User email address
            - password (str): User password
    
    Returns:
        tuple: (tenant, domain) objects created
        
    Raises:
        ValidationError: If user data is invalid
        DatabaseError: If tenant creation fails
    """
    # Implementation here
    pass
```

### Error Handling
```python
def register_user(request):
    try:
        # User registration logic
        user = User.objects.create_user(**user_data)
        return redirect('success')
    except ValidationError as e:
        messages.error(request, f"Validation error: {e}")
        return render(request, 'register.html')
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        messages.error(request, "An unexpected error occurred.")
        return render(request, 'register.html')
```

## 🧪 Testing Guidelines

### Test Structure
```python
# tests/test_views.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from tenants.models import Client, Domain

class RegistrationViewTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.registration_url = reverse('register')
    
    def test_registration_success(self):
        """Test successful user registration."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        }
        
        response = self.client.post(self.registration_url, data)
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Client.objects.filter(schema_name='testuser').exists())
    
    def test_registration_password_mismatch(self):
        """Test registration with password mismatch."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'confirm_password': 'differentpass'
        }
        
        response = self.client.post(self.registration_url, data)
        
        self.assertEqual(response.status_code, 200)  # Form with errors
        self.assertContains(response, "Passwords do not match")
```

### Test Categories
- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Tenant Tests**: Test multitenant functionality

### Test Coverage
- Aim for 80%+ code coverage
- Test both success and failure scenarios
- Test edge cases and boundary conditions
- Test security-related functionality

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test accounts.tests.test_views

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

## 📚 Documentation

### Code Documentation
- Document all public functions and classes
- Use docstrings following Google style
- Include type hints where appropriate
- Document complex algorithms or business logic

### README Updates
- Update README.md for new features
- Include setup instructions for new dependencies
- Update API documentation
- Add examples for new functionality

### Documentation Standards
- Use clear, concise language
- Include code examples
- Update version numbers
- Keep documentation current with code changes

## 🔄 Pull Request Process

### Before Submitting
- [ ] Code follows project coding standards
- [ ] Tests pass and coverage is adequate
- [ ] Documentation is updated
- [ ] Code is properly formatted (Black)
- [ ] No linting errors (Flake8)
- [ ] Feature works as expected

### PR Description Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
```

### Review Process
1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Code Review**: Maintainers review code quality and functionality
3. **Testing**: Manual testing of new features
4. **Approval**: Maintainer approval required for merge

### After Approval
- Squash commits if requested
- Update branch with latest main
- Merge will be handled by maintainers

## 🐛 Issue Reporting

### Bug Reports
Use the bug report template:
```markdown
## Bug Description
Clear description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python Version: [e.g., 3.12.0]
- Django Version: [e.g., 5.2.0]
- Browser: [e.g., Chrome 120, Firefox 119]

## Additional Context
Any other context about the problem.
```

### Feature Requests
Use the feature request template:
```markdown
## Feature Description
Clear description of the feature.

## Use Case
Why is this feature needed?

## Proposed Solution
How should this feature work?

## Alternatives Considered
Other solutions you've considered.

## Additional Context
Any other context about the feature request.
```

## 🏷️ Labels and Milestones

### Issue Labels
- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information is requested

### Milestones
- `v1.0.0`: Initial stable release
- `v1.1.0`: Minor feature release
- `v2.0.0`: Major feature release

## 🎯 Contribution Areas

### High Priority
- Bug fixes and security patches
- Performance improvements
- Documentation improvements
- Test coverage improvements

### Medium Priority
- New features
- UI/UX improvements
- API enhancements
- Code refactoring

### Low Priority
- Nice-to-have features
- Experimental features
- Cosmetic changes

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Request Comments**: Code-specific discussions

### Response Times
- **Critical Bugs**: 24-48 hours
- **Regular Issues**: 3-5 business days
- **Feature Requests**: 1-2 weeks
- **Pull Requests**: 3-7 business days

## 🏆 Recognition

### Contributors
- All contributors will be listed in CONTRIBUTORS.md
- Significant contributors may be added to the project team
- Contributors will be acknowledged in release notes

### Contribution Types
- Code contributions
- Documentation improvements
- Bug reports
- Feature suggestions
- Community support

## 📄 License

By contributing to EchoBlogs, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🙏 Thank You

Thank you for contributing to EchoBlogs! Your contributions help make this project better for everyone. We appreciate your time and effort in improving the multitenant blogging platform.

---

**Happy Contributing! 🚀**
