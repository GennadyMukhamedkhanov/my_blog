from rest_framework import permissions


class OnlyReadOrIsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)



class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author

class IsAuthorComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user