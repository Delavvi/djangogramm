from django.test import TestCase, Client
from polls.views import create_newsfeed, NewsFeedList, news_like, news_dislike
from django.urls import reverse
from polls.forms import RegisterForm
from polls.models import Profile, GramPost
import bs4
from django.contrib.auth.models import User


class RegisterUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.name = 'test'
        self.password = 'password123'

    def test_register_get(self):
        response = self.client.get(reverse("polls:register"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='polls/register.html')

    def test_register_post_success(self):
        response = self.client.post(reverse("polls:register"), data={'name': self.name, 'password1': self.password,
                                                                     'password2': self.password})
        self.assertEquals(response.status_code, 302)

    def test_register_post_fail(self):
        response = self.client.post(reverse("polls:register"), data={'name': self.name, 'password1': self.password,
                                                                     'password2': 'wrong'})
        self.assertEquals(response.status_code, 200)
        form = response.context.get('form')
        self.assertFalse(form.is_valid())

    def test_confirm_email_get(self):
        response = self.client.get(reverse('polls:email', kwargs={'name': self.name, 'password': self.password}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='polls/email.html')

    def test_confirm_email_post(self):
        response = self.client.post(reverse('polls:email', kwargs={'name': self.name, 'password': self.password}),
                                    data={'email': 'testuser@gmail.com'})
        self.assertEquals(response.status_code, 200)
        users = User.objects.get()
        self.assertIsNotNone(users)


class HomePageTest(TestCase):
    def setUp(self):
        self.user_name = "test"
        self.user_password = "password123"
        user = User.objects.create_user(username=self.user_name, password=self.user_password, email='gh@gmail.com', is_active=True)
        profile = Profile.objects.get(user_id=user)
        profile.name = 'test'
        profile.avatar = 'media/test/tree-736885_1280.jpg'
        profile.bio = "funny_bio"
        profile.save()
        post = GramPost.objects.create(name='some_name', description='some_description', tags=['1', '2'], user_id=user)
        self.client.login(username=self.user_name, password=self.user_password)

    def test_get_home_page(self):
        response = self.client.get(reverse('polls:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('polls/home.html')

    def test_check_profile(self):
        response = self.client.get(reverse('polls:home'))
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        profile_ = soup.find('div', class_='profile-card')
        self.assertIn(self.user_name, str(profile_))
        self.assertIn("funny_bio", str(profile_))

    def test_show_post(self):
        response = self.client.get(reverse('polls:home'))
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        post = soup.find('div', class_="article")
        self.assertIn('some_name', str(post))

    def test_new_post_get(self):
        response = self.client.get(reverse('polls:new-post'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('polls/post.html')

    def test_new_post_post(self):
        response = self.client.post(reverse('polls:new-post'), data={'name': "some_name",
                                                                     'description': "some_description", 'tags': ['1', '2']})
        self.assertEquals(response.status_code, 302)
        post = GramPost.objects.filter(name='some_name')
        self.assertIsNotNone(post)