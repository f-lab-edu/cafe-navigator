from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from utils.permissions import IsOwnerOrReadOnly, IsAdminUser
from utils.viewsets import ModelWithoutListViewSet
from cafe.models import Cafe, Comment, Like
from cafe.serializers import CafeSerializers, CommentSerializers, LikeSerializers


class CafeViewSet(ModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializers

    def perform_create(self, serializer):
        serializer.save(staff=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CommentViewSet(ModelWithoutListViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.request.method == 'PUT':
            permission_classes = [IsOwnerOrReadOnly]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAdminUser, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)