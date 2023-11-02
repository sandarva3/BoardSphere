from django.test import TestCase
from django.urls import reverse, resolve
from .views import home_view, board_view, newTopic_view
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm

class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.response = self.client.get(reverse('home'))

    def test_home_view_status_and_resolves(self):
        self.assertEquals(self.response.status_code, 200)
        self.assertEquals(resolve('/').func, home_view)

    def test_home_view_contains_link_to_topics_page(self):
        self.assertContains(self.response, 'href="{0}"'.format(reverse('board_topics', kwargs={'pk': self.board.pk})))

class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Django Board", description="This is the description.")
    
    def test_board_view_status_codes(self):
        response = self.client.get(reverse('board_topics', kwargs={'pk': self.board.pk}))
        self.assertEquals(response.status_code, 200)
        
        response = self.client.get(reverse('board_topics', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 404)
    
    def test_board_view_resolves_and_contains_links(self):
        response = self.client.get(reverse('board_topics', kwargs={'pk': self.board.pk}))

        self.assertEquals(resolve('/board/1/').func, board_view)
        self.assertContains(response, 'href="{0}"'.format(reverse('home')))
        self.assertContains(response, 'href="{0}"'.format(reverse('newtopic', kwargs={'pk': self.board.pk})))

class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='123')