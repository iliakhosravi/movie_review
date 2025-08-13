from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'movie', 'text', 'rating', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
