from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post, Comment
from django.contrib.auth.models import User

class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)

    def test_create_post(self):
        response = self.client.post(reverse('post-list-create'), {'title': 'New Post', 'content': 'New content.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_get_posts(self):
        response = self.client.get(reverse('post-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_post_details(self):
        response = self.client.get(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)

    def test_update_post(self):
        response = self.client.put(reverse('post-detail', args=[self.post.id]), {'title': 'Updated Title', 'content': 'Updated content.'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_delete_post(self):
        response = self.client.delete(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)
        self.comment = Comment.objects.create(post=self.post, text='This is a comment.', author=self.user)

    def test_add_comment(self):
        response = self.client.post(reverse('comment-list-create', args=[self.post.id]), {'text': 'New comment.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_get_comments(self):
        response = self.client.get(reverse('comment-list-create', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_can_only_see_own_comments(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpass')
        Comment.objects.create(post=self.post, text='Another user comment.', author=another_user)
        response = self.client.get(reverse('comment-list-create', args=[self.post.id]))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], self.comment.text)

    def test_update_comment(self):
        response = self.client.put(reverse('comment-detail', args=[self.post.id, self.comment.id]), {'text': 'Updated Comment'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Updated Comment')

    def test_delete_comment(self):
        response = self.client.delete(reverse('comment-detail', args=[self.post.id, self.comment.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())