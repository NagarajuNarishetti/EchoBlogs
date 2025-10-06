from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),           # home, login, logout, register
    path('blog/', include('blog.urls')),          # tenant-specific blog posts
]
