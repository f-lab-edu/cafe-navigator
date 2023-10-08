from rest_framework.exceptions import ValidationError
from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

from cafe.models import Cafe, Comment, Like
from cafe.serializers import CafeSerializers, CommentSerializers, LikeSerializers


class CafeViewSet(ModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializers
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(staff=self.request.user)


class CafeSearchViewSet(ReadOnlyModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        print(self.queryset)
        return self.queryset.filter(name=self.kwargs.get("search"))


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    
    def get_queryset(self):
        return self.queryset.filter(cafe=self.kwargs.get("cafe_id"))

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            cafe=Cafe.objects.get(id=self.kwargs.get("cafe_id"))
        )
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'OPTIONS']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.request.method in ['PUT', 'PATCH']:
            permission_classes = [IsOwnerOrReadOnly]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAdminOrReadOnly, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers
    
    def get_queryset(self):
        return self.queryset.filter(cafe=self.kwargs.get("cafe_id"))

    def perform_create(self, serializer):
        user = self.request.user
        cafe = Cafe.objects.get(id=self.kwargs.get("cafe_id"))

        if Like.objects.get(user=user, cafe=cafe):
            raise ValidationError(detail='이미 좋아요 누른 게시물입니다.')

        serializer.save(
            user=user,
            cafe=cafe
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]