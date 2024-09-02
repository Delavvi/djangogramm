from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("sign/", views.MyLogInView.as_view(), name='sign'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("home/", views.HomePage.as_view(), name='home'),
    path("home/<str:post_filter>", views.HomePage.as_view(), name='home'),
    path("confirm-email/<str:name>/<str:password>/<str:email>", views.EmailView.as_view(), name='email'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
    path('profile/', views.MyProfile.as_view(), name='profile'),
    path('new-post/', views.PostCreate.as_view(), name='new-post'),
    path('likes/<int:pk>', views.like_post, name='likes'),
    path('dislikes/<int:pk>', views.post_dislike, name='dislikes'),
    path('home/<int:pk>/', views.HomePage.as_view(), name='home'),
    path('new-tags/<int:pk>', views.add_new_tags, name='new_tags'),
    path('subscribe/<int:user_id>', views.subscribe, name='subscribe'),
    path('news', views.NewsFeedList.as_view(), name='news-feed'),
    path('news-likes/<int:pk>', views.news_like, name='news-likes'),
    path('news-dislikes/<int:pk>', views.news_dislike, name='news-dislikes'),
    path('create-news', views.NewsCreate.as_view(), name='create-news'),
    path('user-details/<int:user_id>', views.UserInformation.as_view(), name='user-details'),
]
