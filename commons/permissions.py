from api.category.models import Category
from api.board.models import Item

from rest_framework.permissions import BasePermission

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

class CategoryAccessPermission(BasePermission):

    message = "This user doesn't have access permission for this category!"

    def has_permission(self, request, view):
        category_id = view.kwargs.get("id")
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return False
        
        user = User.objects.get(username=request.user)
        if user.is_superuser:
            return True
        try:
            category.user_accesses.get(username=user.username)
            return True
        except User.DoesNotExist:
            return False

class ItemAccessPermission(BasePermission):

    message = "This user doesn't have access permission for this item!"

    def has_permission(self, request, view):
        item_id = view.kwargs.get("id")
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return False
        
        user = User.objects.get(username=request.user)
        if user.is_superuser:
            return True
        elif user == item.owner:
            return True
        else:
            return False
