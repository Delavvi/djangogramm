from django import forms
from django.core.exceptions import ValidationError
from .models import Profile, GramPost, FeedPost
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']
        widgets = {'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}),
                   'password2': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'}),
                   'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'})}

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError("Taken Email")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = 'register'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))


class SignForm(AuthenticationForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.helper = FormHelper()
        self.helper.form_tag = 'sign'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))


class FormEmail(forms.Form):
    email = forms.EmailField(label='email')


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file', 'id': 'avatar'}), label='avatar')
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), label='bio')
    name = forms.CharField(label='name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'name']
        widgets = {'avatar': forms.FileInput(attrs={'class': 'form-control-file', 'id': 'avatar'}),
                   'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'name': forms.TextInput(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = 'profile-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit("submit", "Save"))


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CreatePost(forms.ModelForm):
    name = forms.CharField(max_length=100,
                               required=True, label='name')
    description = forms.CharField(max_length=100, label='description',
                           required=True,
                           )
    photo = MultipleFileField()

    class Meta:
        model = GramPost
        fields = ['name', 'description', 'tags']


class CreateNewsForm(forms.ModelForm):
    photo = MultipleFileField()

    class Meta:
        model = FeedPost
        fields = ['description']
