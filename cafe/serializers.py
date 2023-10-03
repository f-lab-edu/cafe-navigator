from rest_framework import serializers
from cafe.models import Cafe, Comment, Like


class CafeSerializers(serializers.ModelSerializer):
    staff  = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Cafe
        fields = '__all__'


class CommentSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = '__all__'