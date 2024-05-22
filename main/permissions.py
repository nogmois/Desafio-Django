# Classe de permissão personalizada para garantir que apenas o criador de um projeto possa modificá-lo.

from rest_framework import permissions

class IsProjectOwner(permissions.BasePermission):
    message = 'You must be the creator of this project to modify it.'

    def has_object_permission(self, request, view, obj):
        # Verifica se o usuário atual é o criador do projeto
        return obj.creator == request.user
