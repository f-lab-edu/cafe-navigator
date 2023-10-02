from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from user.models import User


@api_view(['POST'])
def sign_up(request):
    username = request.data.get("username")
    password = request.data.get("password")
    User.objects.create_user(username=username, password=password)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)