from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import render
from django.contrib.auth.views import LoginView

def home(request):
    """
    Представление для отображения главной страницы.
    """
    return render(request, 'blog/base.html')

class PostListCreateView(generics.ListCreateAPIView):
    """
    API для получения списка постов и создания нового поста.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Убедитесь, что это указано

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API для получения, обновления и удаления поста.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class CommentListCreateView(generics.ListCreateAPIView):
    """
    Представление для получения списка комментариев и создания нового комментария.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает список комментариев для указанного поста.
        """
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """
        Создаёт новый комментарий, связывая его с текущим пользователем и постом.
        """
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления комментария.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает комментарии, принадлежащие текущему пользователю.
        """
        return Comment.objects.filter(author=self.request.user)

class UserCommentListView(generics.ListAPIView):
    """
    API для получения списка всех комментариев текущего пользователя.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

class CustomLoginView(LoginView):
    """
    Кастомизированное представление для входа пользователей.
    """
    template_name = 'blog/login.html'  # Указываем ваш шаблон