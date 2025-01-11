from rest_framework.permissions import BasePermission

class IsSecretary(BasePermission):
    """
    Permite acces doar utilizatorilor cu rolul 'Secretary'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Secretary'


class IsProfessor(BasePermission):
    """
    Permite acces doar utilizatorilor cu rolul 'Professor'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Professor'


class IsStudent(BasePermission):
    """
    Permite acces doar utilizatorilor cu rolul 'Student'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Student'
    

class IsStudentRepresentative(BasePermission):
    """
    Permite acces doar utilizatorilor cu rolul 'StudentRepresentative'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'StudentRepresentative'