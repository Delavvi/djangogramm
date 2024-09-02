from django.contrib import admin
from .models import Followers, ConfirmEmail, GramPost, Photos, Profile, FeedPhotos, FeedPost


admin.site.register(Followers)
admin.site.register(ConfirmEmail)
admin.site.register(GramPost)
admin.site.register(Photos)
admin.site.register(Profile)
admin.site.register(FeedPhotos)
admin.site.register(FeedPost)
