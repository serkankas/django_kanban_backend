import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User

from commons.permissions import UserAccessPermission
from commons.functions import check_desired_field, check_user_uniqueness, user_id_and_username_check, check_password_quality

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request, *args, **kwargs):
    data = User.objects.all()
    model = []
    for user in data:
        model.append([user.pk, user.username])
    return Response(data=model, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, UserAccessPermission])
def get_user_information(request, *args, **kwargs):
    user_id = kwargs['id']
    try:
        data = User.objects.get(pk=user_id)
        model = {
            'id':data.pk,
            'username':data.username,
            'first_name':data.first_name,
            'last_name':data.last_name,
            'email':data.email,
        }
    except User.DoesNotExist:
        model = {"message":"There is no such user."}
    return Response(data=model, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_user_information(request, *args, **kwargs):
    desired_fields = ['username', 'first_name', 'last_name', 'email', 'password']
    captured_fields = json.loads(request.body.decode())
    r_data, r_status = check_desired_field(desired_fields, captured_fields)
    if r_data != None:
        return Response(data=r_data, status=r_status)

    username = captured_fields["username"]
    if check_user_uniqueness(username):
        user = User.objects.create_user(**captured_fields)
        return Response(data={"message":f"The {username} is succesfully created!"}, status=status.HTTP_201_CREATED)
    else:
        return Response(data={"message":f"The username {username} is already taken!"}, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, UserAccessPermission])
def update_user_information(request, *args, **kwargs):
    desired_fields = ['id', 'username', 'first_name', 'last_name', 'email']
    captured_fields = json.loads(request.body.decode())
    r_data, r_status = check_desired_field(desired_fields, captured_fields)
    if r_data != None:
        return Response(data=r_data, status=r_status)
    username = captured_fields["username"]
    user_id = captured_fields["id"]
    try:
        if user_id_and_username_check(user_id, username):
            user = User(**captured_fields)
            user.save()
            return Response({"message": f"The {username} has succesfully updated!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"The username and ID is not matching!"}, status=status.HTTP_400_BAD_REQUEST)
    except (ValueError, KeyError, TypeError):
        return Response({"message": "Update process has been uncompleted!"}, status=status.HTTP_410_GONE)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, UserAccessPermission])
def delete_user_information(request, *args, **kwargs):
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return Response({"message":"User has been deleted already!"}, status=status.HTTP_410_GONE)
    username = user.username
    user.delete()
    return Response({"message":f"The user {username} has been deleted succesfully"}, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, UserAccessPermission])
def change_user_password(request, *args, **kwargs):
    desired_fields = ['id', 'username', 'password']
    captured_fields = json.loads(request.body.decode())
    r_data, r_status = check_desired_field(desired_fields, captured_fields)
    if r_data != None:
        return Response(data=r_data, status=r_status)

    username = captured_fields["username"]
    user_id = captured_fields["id"]
    if user_id_and_username_check(user_id, username):
        user = User.objects.get(username=username)
        password = captured_fields["password"]
        if check_password_quality(password):
            user.set_password(password)
            return Response({"message": f"The user {username}'s password changed successfully!"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message": f"Couldn't pass the quality control"}, status=status.HTTP_400_BAD_REQUEST)
