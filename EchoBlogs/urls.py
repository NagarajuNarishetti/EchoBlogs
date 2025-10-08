from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# API routers
from blog.api_urls import router as blog_api_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),           # home, login, logout, register
    path('blog/', include('blog.urls')),          # tenant-specific blog posts
    # API routes
    path('api/', include('accounts.api_urls')),
    path('api/', include(blog_api_router.urls)),
]
