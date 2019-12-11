
from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

class IsNotAnonymousUser(permissions.BasePermission):
    message = 'Anonymous users are not allowed'

    def has_permission(self, request, view):
        return (type(request.user) is not AnonymousUser)