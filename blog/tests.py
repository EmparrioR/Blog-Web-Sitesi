

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(author=self.user, title='Test Post', content='Test Content')

    def test_authenticated_user_can_add_comment(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post_detail', args=[self.post.pk]), {'text': 'This is a comment.'})
        self.assertEqual(response.status_code, 302)  # Beklenen: Yorum ekledikten sonra yönlendirme
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, 'This is a comment.')

    def test_anonymous_user_cannot_add_comment(self):
        response = self.client.post(reverse('post_detail', args=[self.post.pk]), {'text': 'This is an anonymous comment.'})
        self.assertEqual(response.status_code, 302)  # Beklenen: Yorum ekledikten sonra yönlendirme
        self.assertEqual(Comment.objects.count(), 0)  # Anonim kullanıcı yorum ekleyemez
