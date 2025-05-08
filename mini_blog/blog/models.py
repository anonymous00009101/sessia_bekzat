from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    Модель для постов блога.
    """
    title = models.CharField(max_length=255)  # Заголовок поста
    content = models.TextField()  # Содержимое поста
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор поста
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания поста

    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    Модель для комментариев к постам.
    """
    text = models.TextField()  # Текст комментария
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  # Связь с постом
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания комментария

    def __str__(self):
        return self.text[:20]  # Возвращает первые 20 символов текста комментария