from rest_framework import viewsets
from rest_framework import permissions
from cafe.permissions import IsOwnerOrReadOnly
from cafe.models import Cafe, Comment, Like
from cafe.serializers import CafeSerializers, CommentSerializers, LikeSerializers


class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializers

    def perform_create(self, serializer):
        serializer.save(staff=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)