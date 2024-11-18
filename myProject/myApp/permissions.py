from rest_framework.permissions import BasePermission

class IsSecretary(BasePermission):
    """
    Permite acces doar utilizatorilor cu rolul 'Secretary'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Secretary'
