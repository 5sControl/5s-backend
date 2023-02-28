from rest_framework import permissions

from django.contrib.auth.models import User

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return User.objects.filter(username=request.user)


class IsSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff