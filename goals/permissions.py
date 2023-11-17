from rest_framework import permissions


class IsUserLogged(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.id and request.user.is_authenticated


class IsOwnerOfGoal(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user and request.user.is_authenticated
