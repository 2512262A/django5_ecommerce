from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to edit objects.
    """

    def has_permission(self, request, view):
        # Allow read-only access for all users (safe methods)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow CUD operations for superusers
        return request.user and request.user.is_superuser
