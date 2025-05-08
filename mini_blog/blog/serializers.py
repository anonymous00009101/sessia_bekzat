from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.
    """
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author']  # Поля для сериализации
        read_only_fields = ['id', 'created_at', 'author']  # Поля только для чтения

class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    """
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'author', 'post']  # Поля для сериализации
        read_only_fields = ['id', 'created_at', 'author', 'post']  # Поля только для чтения