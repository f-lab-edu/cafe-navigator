from rest_framework import serializers
from cafe.models import Cafe, Comment, Like 


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = '__all__'


class CafeSerializer(serializers.ModelSerializer):
    staff  = serializers.ReadOnlyField(source='user.username')
    like_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Cafe
        fields = '__all__'

    def get_like_count(self, obj):
        return Like.objects.filter(cafe=obj).count()
    
    def get_comments(self, obj):
        comments = Comment.objects.filter(cafe=obj)
        return CommentSerializer(comments, many=True).data