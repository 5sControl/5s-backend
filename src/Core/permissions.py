from rest_framework import permissions

from src.Employees.models import CustomUser


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return CustomUser.objects.filter(username=request.user)


class IsSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.ADMIN


class IsStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class IsAdminOrSuperuserPermission(permissions.BasePermission):
    """
    Permission to allow access to users with the 'superuser' or 'admin' role.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == CustomUser.SUPERUSER or request.user.role == CustomUser.ADMIN)
        )
