from rest_framework import permissions

class IsBlogWriter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_blog_writer