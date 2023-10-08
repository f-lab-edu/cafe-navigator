from django.contrib.auth import login, logout, authenticate
from django.db.utils import IntegrityError

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework import generics, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from utils.permissions import IsOwnerOrReadOnly
from user.models import User
from user.serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsOwnerOrReadOnly]


@api_view(['POST'])
def sign_up_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    is_staff = request.data.get("is_staff")
    User.objects.create_user(username=username, password=password, is_staff=is_staff)
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