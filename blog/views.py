from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post

def post_list(request):
    """Display all blog posts for the current tenant"""
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'accounts/blog/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    """Create a new blog post"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            Post.objects.create(title=title, content=content, author=request.user)
            messages.success(request, 'Post created successfully!')
            return redirect('post_list')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'accounts/blog/post_create.html')
