from rest_framework import status

from django.contrib.auth.models import User
from django.db.models import Q

from api.category.models import Category

def check_desired_field(desired, captured):
    return_dict = {}
    try:
        for item in captured:
            if not item in desired:
                raise KeyError
        if len(captured) != len(desired):
            raise ValueError
    except KeyError:
        return_dict = {
            "message":"Key Error",
            "unmatched_key": item
        }

        return return_dict, status.HTTP_400_BAD_REQUEST

    except ValueError:
        _missing_keys = []
        for item in desired:
            if not item in captured:
                _missing_keys.append(item)
        
        return_dict = {
            "message":"Missing Key/s",
            "missing_keys":_missing_keys
        }

        return return_dict, status.HTTP_400_BAD_REQUEST

    return None, status.HTTP_200_OK

def check_user_uniqueness(username):
    try:
        User.objects.get(username=username)
        return False
    except User.DoesNotExist:
        return True

def user_id_and_username_check(user_id, user_username):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return False
    
    if user_username != user.username:
        return False
    else:
        return True

def check_password_quality(password):
    return True

def check_category_uniqueness(category_title, username):
    existance = Category.objects.filter(
        Q(user_accesses=username) & Q(category_title=category_title)
    ).count()

    if existance:
        return False
    else:
        return True
