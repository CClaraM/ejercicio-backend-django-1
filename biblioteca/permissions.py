from rest_framework.permissions import BasePermission

class IsAdminRol(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and getattr(user, 'rol', '') == 'admin'
        )