from rest_framework import permissions

class IsProjectOwner(permissions.BasePermission):
    message = 'You must be the creator of this project to modify it.'

    def has_object_permission(self, request, view, obj):
        # Ensure that the project's creator is the current user
        return obj.creator == request.user
