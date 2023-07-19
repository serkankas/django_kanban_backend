import json
import datetime

from .models import Item
from api.category.models import Category

from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from commons.functions import check_desired_field, check_item_uniqueness, check_category_permission
from commons.permissions import ItemAccessPermission

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_list(request, *args, **kwargs):
    return_dict = {}
    raw_data = Item.objects.filter(owner=request.user)

    if raw_data.exists():
        return_dict = {"message":"Successfully fetch the items.", "items":{}}
        for item in raw_data:
            return_dict["items"][item.id] = {
                "id":item.id,
                "item_id":item.item_id,
                "item_title":item.item_title,
                "item_description":item.item_description,
                "order_id":item.order_id,
                "category_id":item.category.pk
            }
    else:
        return_dict = {"message":"This user doesn't have any created item yet.", "categories":{}}

    return Response(data=return_dict, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, ItemAccessPermission])
def get_item_information(request, *args, **kwargs):
    item_id = kwargs['id']
    try:
        raw_data = Item.objects.get(pk=item_id)
        model = raw_data.__dict__
        model.pop('_state')
    except Item.DoesNotExist:
        model = {"message":"There is no such a item!"}
    
    return Response(data=model, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, ItemAccessPermission])
def update_item_information(request, *args, **kwargs):
    item_id = kwargs['id']
    desired_fields = ['item_title', 'item_description', 'order_id', 'category_id']
    captured_fields = json.loads(request.body.decode())
    r_data, r_status = check_desired_field(desired_fields, captured_fields)
    if r_data != None:
        return Response(data=r_data, status=r_status)
    
    try:
        category = Category.objects.get(pk=captured_fields['category_id'])
    except Category.DoesNotExist:
        return Response({"message": "This user cannot create item in this category."}, status=status.HTTP_406_NOT_ACCEPTABLE)


    item = Item.objects.get(pk=item_id)
    item.order(captured_fields["order_id"])
    item.item_title = captured_fields['item_title']
    item.item_description = captured_fields['item_description']
    item.category = category
    item.save()

    return Response({"message":f"Item {item.item_title} is succesfully changed!"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item_information(request, *args, **kwargs):
    desired_fields = ['item_title', 'item_description', 'category_id']
    captured_fields = json.loads(request.body.decode())
    r_data, r_status = check_desired_field(desired_fields, captured_fields)
    if r_data != None:
        return Response(data=r_data, status=r_status)

    user = User.objects.get(username=request.user)
    category_id = captured_fields["category_id"]
    order = Item.count(user, category_id) + 1
    title = captured_fields['item_title']
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response({"message": "This user cannot create item in this category."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    item_id = Item.get_next_id() + 1
    if check_category_permission(category_id, user):
        return Response({"message": "This user cannot create item in this category."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    if check_item_uniqueness(title, user):
        item = Item.objects.create(**{
            "item_title":title,
            "item_description":captured_fields["item_description"],
            "category":category,
            "owner":user,
            "order_id":order,
            "item_id":item_id,
            "created_date": datetime.datetime.now()
        })

        return Response({"message":f"The {user} created {title} successfully!"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": f"The {user} has already have {title} item"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ItemAccessPermission])
def delete_item_information(request, *args, **kwargs):
    item_id = kwargs['id']
    try:
        item = Item.objects.get(pk=item_id)
        item.delete()

        return Response({"message":f"The {request.user} deleted {item.item_title} succesfully!"}, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({"message":f"There is no item found with the ID:{item_id}"}, status=status.HTTP_400_BAD_REQUEST)
