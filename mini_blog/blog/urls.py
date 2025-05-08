from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('posts/', views.PostListCreateView.as_view(), name='post-list-create'),  # Список и создание постов
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),  # Детали, обновление, удаление поста
    path('posts/<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),  # Список и создание комментариев
    path('posts/<int:post_id>/comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),  # Детали, обновление, удаление комментария
]