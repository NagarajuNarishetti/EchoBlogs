from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Post
from .serializers import PostSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author_id == getattr(request.user, 'id', None)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required")
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.all()


