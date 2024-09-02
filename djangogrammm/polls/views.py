from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, SignForm, FormEmail, CreatePost, UpdateProfileForm, CreateNewsForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from .models import Profile, GramPost, Photos, Followers, FeedPost, FeedPhotos
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.db.models import Count


@login_required
def subscribe(request, user_id):
    if request.method == "POST":
        user = request.user
        following = User.objects.get(pk=user_id)
        checking = Followers.objects.filter(follower=user, following=following).exists()
        if not checking:
            Followers.objects.create(follower=user, following=following)
        else:
            Followers.objects.filter(follower=user, following=following).delete()
        target = request.POST.get('next')
        if target == "home":
            return JsonResponse(data={'subscribe_status': checking}, status=200)
        else:
            return JsonResponse(data={'subscribe_status': checking}, status=200)


@method_decorator(login_required, name='dispatch')
class MyProfile(UpdateView):
    success_url = reverse_lazy('polls:home')
    template_name = 'polls/profile.html'
    form_class = UpdateProfileForm
    model = Profile

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, user=self.request.user)
        return obj


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        request.session['user_id'] = user.pk
        return redirect(reverse('polls:profile'))
    else:
        return HttpResponse('Invalid activation link!')


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'polls/register.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        self.email = form.cleaned_data['email']
        obj = User.objects.create_user(username=username)
        obj.set_password(password)
        obj.save()
        self.password = password
        self.object = obj
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('polls:email', kwargs={'name': self.object.username, 'password': self.password,
                                                   'email': self.email})


class EmailView(TemplateView):
    template_name = 'polls/mail.html'

    def send_activation_email(self):
        name = self.kwargs.get('name')
        password = self.kwargs.get('password')
        user = authenticate(self.request, username=name, password=password)
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        current_site = get_current_site(self.request)
        token = default_token_generator.make_token(user)
        message = render_to_string('polls/email_template.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        mail_subject = 'Activate your account.'
        email = self.kwargs.get('email')
        send_mail(mail_subject, message, 'djangogramm96@gmail.com', [email])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.send_activation_email()
        return context


@login_required
def logout_(request: HttpRequest):
    logout(request)


class MyLogInView(LoginView):
    form_class = SignForm
    template_name = 'polls/log-in.html'
    success_url = reverse_lazy('polls:home')


@method_decorator(login_required, name='dispatch')
class HomePage(ListView):
    paginate_by = 50
    model = GramPost
    template_name = "polls/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_ = Profile.objects.get(user=self.request.user)
        context['name'] = profile_.name
        context['bio'] = profile_.bio
        context['image'] = profile_.avatar
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        friends_posts_checked = 'friends_posts' in self.request.GET
        sort_type = self.request.GET.get('flexRadioDefault', None)
        if friends_posts_checked:
            user = self.request.user
            friends = Followers.objects.filter(follower=user)
            friends_pks = friends.values('following')
            if sort_type == 'popular':
                queryset = GramPost.objects.filter(user_id__in=friends_pks).annotate(
                    likes_count=Count('likes')).order_by('-likes_count')
            else:
                queryset = GramPost.objects.filter(user_id__in=friends_pks).order_by('date')
        else:
            if sort_type == 'popular':
                queryset = GramPost.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')
            else:
                queryset = GramPost.objects.order_by('date')

        return queryset


@login_required
def like_post(request, pk):
    post = get_object_or_404(GramPost, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
    likes = post.likes.count()
    dislikes = post.dislikes.count()
    if likes is None:
        likes = 0
    if dislikes is None:
        dislikes = 0
    return JsonResponse(data={'likes': likes, 'dislikes': dislikes}, status=200)


@login_required
def post_dislike(request, pk):
    post = get_object_or_404(GramPost, id=pk)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
    dislikes = post.dislikes.count()
    likes = post.likes.count()
    return JsonResponse(data={'dislikes': dislikes, 'likes': likes}, status=200)


@method_decorator(login_required, name='dispatch')
class PostCreate(CreateView):
    model = GramPost
    success_url = reverse_lazy('polls:home')
    template_name = 'polls/post.html'
    form_class = CreatePost

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_id = self.request.user
        obj.save()
        photos = self.request.FILES.getlist('photo')
        for photo in photos:
            post_photo = Photos.objects.create(photo=photo, post_id=obj)
        return super().form_valid(form)


@login_required
def add_new_tags(request, pk):
    if request.method == 'POST':
        new_tags: str = request.POST.get('new_tags')
        post = get_object_or_404(GramPost, id=pk)
        tags = []
        while new_tags:
            if ',' in new_tags:
                tag, new_tags = new_tags.split(',', 1)
            else:
                tag = new_tags
                new_tags = None
            tag = tag.strip()
            if tag:
                tags.append(tag)
                post.tags.add(tag)
        return JsonResponse(data={'tags': tags}, status=200)


@method_decorator(login_required, name='dispatch')
class NewsFeedList(ListView):
    model = FeedPost
    template_name = "polls/news.html"
    paginate_by = 100
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        friends = Followers.objects.filter(follower=user)
        friends_pks = friends.values('following')
        queryset = queryset.filter(user_id__in=friends_pks).order_by('date')
        return queryset


@login_required
def news_like(request, pk):
    post = get_object_or_404(FeedPost, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
    likes = post.likes.count()
    dislikes = post.dislikes.count()
    if likes is None:
        likes = 0
    if dislikes is None:
        dislikes = 0
    return JsonResponse(data={'likes': likes, 'dislikes': dislikes}, status=200)


@login_required
def news_dislike(request, pk):
    post = get_object_or_404(FeedPost, id=pk)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
    dislikes = post.dislikes.count()
    likes = post.likes.count()
    return JsonResponse(data={'dislikes': dislikes, 'likes': likes}, status=200)


@method_decorator(login_required, name='dispatch')
class NewsCreate(CreateView):
    model = FeedPost
    success_url = reverse_lazy('polls:news-feed')
    template_name = 'polls/create-news.html'
    form_class = CreateNewsForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_id = self.request.user
        obj.save()
        photos = self.request.FILES.getlist('photo')
        for photo in photos:
            FeedPhotos.objects.create(photo=photo, post_id=obj.pk)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UserInformation(DetailView):
    model = Profile
    pk_url_kwarg = 'user_id'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get(self.pk_url_kwarg)
        user = get_object_or_404(User, pk=user_id)
        profile = get_object_or_404(Profile, user=user)
        return profile

    def render_to_response(self, context, **response_kwargs):
        profile = context['object']
        data = {
            'name': profile.name,
            'bio': profile.bio,
            'avatar': profile.avatar.url
        }
        return JsonResponse(data)


