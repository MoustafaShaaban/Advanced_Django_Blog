from rest_framework import permissions


class PostPermissions(permissions.BasePermission):
    """
    Custom permessions to show blog posts to everyone and to only allow the author of the post to edit it
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        # So we will allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the post:
        return obj.author == request.user
    

class CommentPermissions(permissions.BasePermission):
    """
    Custom permessions to show blog posts to everyone and to only allow the author of the post to edit it
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        # So we will allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the post:
        return obj.user == request.user