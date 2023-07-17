import json

from .models import Category

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.models import User
from commons.functions import check_desired_field, check_category_uniqueness
from commons.permissions import CategoryAccessPermission

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categories_list(request, *args, **kwargs):
    return_dict = {}
    raw_data = Category.objects.filter(user_accesses=request.user)

    if raw_data.exists():
        return_dict = {"message":"Successfully fetch the categories.", "categories":{}}
        for item in raw_data:
            tmp_dict = item.__dict__
            tmp_dict.pop('_state')
            return_dict["categories"][item.order_id] = tmp_dict
            del(tmp_dict)
    else:
        return_dict = {"message":"This user doesn't have any created category yet.", "categories":{}}

    return Response(data=return_dict, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, CategoryAccessPermission])
def get_category_information(request, *args, **kwargs):
    category_id = kwargs['id']
    try:
        raw_data = Category.objects.get(pk=category_id)
        model = raw_data.__dict__
        model.pop('_state')
    except Category.DoesNotExist:
        model = {"message":"There is no such a category!"}
    
    return Response(data=model, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, CategoryAccessPermission])
def update_category_information(request, *args, **kwargs):
    desired_fields = ['id', 'category_title', 'order_id']
    captured_fields = json.loads(request.body.decode())
    r_data, r_status = check_desired_field(desired_fields, captured_fields)
    if r_data != None:
        return Response(data=r_data, status=r_status)

    category = Category.objects.get(pk=captured_fields['id'])
    category.order(captured_fields["order_id"])
    category(**captured_fields)
    category.save()

    return Response({"message":f"Category {category.category_title} is succesfully changed!"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category_information(request, *args, **kwargs):
    desired_fields = ['category_title']
    captured_fields = json.loads(request.body.decode())
    r_data, r_status = check_desired_field(desired_fields, captured_fields)
    if r_data != None:
        return Response(data=r_data, status=r_status)

    user = request.user
    order = Category.count(user) + 1
    title = captured_fields['category_title']
    if check_category_uniqueness(title, user):
        category = Category.objects.create(**{
            "category_title":title,
            "user_accesses":user,
            "order_id":order
        })

        return Response({"message":f"The {user} created {category.category_title} successfully!"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": f"The {user} has already have {title} category"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, CategoryAccessPermission])
def delete_category_information(request, *args, **kwargs):
    category_id = kwargs['id']
    try:
        category = Category.objects.get(pk=category_id)
        category.delete()

        return Response({"message":f"The {request.user} deleted {category.category_title} succesfully!"}, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({"message":f"There is no category found with the ID:{category_id}"}, status=status.HTTP_400_BAD_REQUEST)
