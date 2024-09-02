from django.core.management.base import BaseCommand
from ...models import Profile, GramPost, Photos
from django.contrib.auth.models import User
from faker import Faker
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

profile_images = [
    'media/test/images (3).jpg'
]

post_images = [
    'media/test/images (3).jpg'
]


def create_test_data(user_num: int):
    '''
    creates fake data
    '''
    fake = Faker()
    random.seed(10)
    Faker.seed(42)
    user = []
    profile = []
    posts = []
    while user_num > 0:
        one_char_name = fake.name()
        one_char_email = fake.email()
        password = fake.password()
        user_info = {"name": one_char_name, "email": one_char_email, "password": password}
        user.append(user_info)
        profile_name = fake.name()
        bio = fake.text()
        avatar = random.choice(profile_images)
        profile_info = {'name': profile_name, 'bio': bio, 'avatar': avatar}
        profile.append(profile_info)
        random_number = random.choice([0, 5])
        post_name = fake.name()
        post_pictures = random.choice(post_images)
        random_tags = [fake.word() for _ in range(random_number)]
        description = fake.text()
        post_info = {'name': post_name, 'picture': post_pictures, 'tags': random_tags, 'description': description}
        posts.append(post_info)
        user_num -= 1
    return user, profile, posts


class Command(BaseCommand):
    help = 'fills database'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user, self.profile, self.posts = create_test_data(20)

    def create_users(self):
        '''
        fills database
        '''
        User.objects.all().delete()
        Profile.objects.all().delete()
        GramPost.objects.all().delete()
        for ind in range(len(self.user)):
            user = User.objects.create_user(
                username=self.user[ind]['name'],
                password=self.user[ind]['password'],
                email=self.user[ind]['email']
            )
            profile = Profile.objects.get(user=user)
            profile.bio = self.profile[ind]['bio']
            profile.name = self.profile[ind]['name']
            profile.avatar = self.profile[ind]['avatar']
            post = GramPost.objects.create(
                user_id=user,
                description=self.posts[ind]['description'],
                name=self.posts[ind]['name'],
                tags=self.posts[ind]['tags']
            )
            photo = Photos.objects.create(
                post_id=post,
                photo=self.posts[ind]['picture']
            )

    def handle(self, *args, **kwargs):
        self.create_users()



