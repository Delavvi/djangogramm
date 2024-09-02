from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from django.utils.text import slugify


class BasePhoto(models.Model):
    photo = models.ImageField(null=True, blank=True, upload_to='media/feeds')
    small_photo = models.ImageField(null=True, blank=True, upload_to='media/feeds')

    def save(self, *args, **kwargs):
        if self.photo and not self.small_photo:
            img = Image.open(self.photo)
            img.thumbnail((300, 300))
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            thumbnail_image = InMemoryUploadedFile(thumb_io, None, 'thumbnail.jpg', 'image/jpeg', thumb_io.tell(), None)
            self.small_photo.save('thumbnail.jpg', thumbnail_image, save=False)
            super().save(*args, **kwargs)

    class Meta:
        abstract = True


class BasePost(models.Model):
    description = models.TextField(default=None)
    date = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class FeedPost(BasePost):
    likes = models.ManyToManyField(User, related_name='feed_likes')
    dislikes = models.ManyToManyField(User, related_name='feed_dislikes')


class FeedPhotos(BasePhoto):
    post = models.ForeignKey(FeedPost, related_name='images', on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True, upload_to='media/feeds')
    small_photo = models.ImageField(null=True, blank=True, upload_to='media/feeds')


class GramPost(BasePost):
    name = models.CharField(max_length=70, null=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name


class Photos(BasePhoto):
    photo = models.ImageField(null=True, blank=True, upload_to='media/images')
    post_id = models.ForeignKey(GramPost, on_delete=models.CASCADE, related_name='post_id')


class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')


class ConfirmEmail(models.Model):
    confirm_email = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="Anonymous")
    avatar = models.ImageField(null=True, upload_to='media/avatar')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Profile, self).save(*args, **kwargs)
