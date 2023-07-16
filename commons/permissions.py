from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from rest_framework import status

from django.contrib.auth.models import User

class UserAccessPermission(BasePermission):

    message = "This user doesn't have access permission!"

    def has_permission(self, request, view):
        user_id = view.kwargs.get("id")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return False
        
        if User.objects.get(username=request.user).is_superuser:
            return True
        elif request.user == user:
            return True
        else:
            return False
