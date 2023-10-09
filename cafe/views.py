from django.db.models import Q

from rest_framework.exceptions import ValidationError
from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geopy.geocoders import Nominatim

from utils.permissions import IsOwner, IsAdminOrReadOnly

from cafe.models import Cafe, Comment, Like
from cafe.serializers import CafeSerializer, CommentSerializer, LikeSerializer


class CafeViewSet(ModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def geocoding(address):
    geolocoder = Nominatim(user_agent='South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    return geo.latitude, geo.longitude


class CafeSearchViewSet(ListAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        location = self.request.query_params.get('location', None)
        longitude = self.request.query_params.get('longitude', None)
        latitude = self.request.query_params.get('latitude', None)
        capacity = self.request.query_params.get('capacity', None)
        outlet = self.request.query_params.get('outlet', None)
        floor = self.request.query_params.get('floor', None)

        cafe_condition = Q()

        if name:
            cafe_condition.add(Q(name__icontains=name), Q.AND)

        if location:
            latitude, longitude = geocoding(location)

        if latitude and longitude:
            cafe_condition.add(
                Q(latitude__range=(latitude - 0.009, latitude + 0.009), longitude__range=(longitude - 0.009, longitude + 0.009)), Q.AND
            )
        
        if capacity:
            cafe_condition.add(Q(capacity__gt=capacity), Q.AND)

        if outlet:
            cafe_condition.add(Q(outlet=outlet), Q.AND)
        
        if floor:
            cafe_condition.add(Q(floor=floor), Q.AND)

        queryset = Cafe.objects.filter(cafe_condition).distinct()
        return queryset


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return self.queryset.filter(cafe=self.kwargs.get("cafe_id"))

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            cafe=Cafe.objects.get(id=self.kwargs.get("cafe_id"))
        )
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            permission_classes = [IsOwner]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAdminUser|IsOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    def get_queryset(self):
        return self.queryset.filter(cafe=self.kwargs.get("cafe_id"))

    def perform_create(self, serializer):
        user = self.request.user
        cafe = Cafe.objects.get(id=self.kwargs.get("cafe_id"))

        if Like.objects.filter(user=user, cafe=cafe).exists():
            raise ValidationError(detail='이미 좋아요 누른 게시물입니다.')

        serializer.save(
            user=user,
            cafe=cafe
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]