from user.models import User
from rest_framework import serializers
from cafe.models import Comment, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password','is_staff']