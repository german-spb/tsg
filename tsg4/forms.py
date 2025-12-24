from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from tinymce.widgets import TinyMCE

from .models import Documents, BlogPost, Comment
from django_summernote.widgets import SummernoteWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from django_recaptcha.fields import ReCaptchaField
from django_password_eye.fields import PasswordEye


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label='Пользователь',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя /или Ник/ или Квартира_...(без пробелов)'
        })
    )
    email = forms.EmailField(

        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )

    def clean_email(self) -> str:
        """Проверяет, что email уникален."""
        email: str = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():  # iexact для регистронезависимого поиска
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    password1 = PasswordEye(label='')
    # password1 = forms.CharField(
    #     max_length=128,
    #     label='Пароль',
    #     widget=forms.PasswordInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Введите пароль'
    #     })
    # )
    password2 = PasswordEye(label='')
    # password2 = forms.CharField(
    #     max_length=128,
    #     label='Подтверждение пароля',
    #     widget=forms.PasswordInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Повторите пароль'
    #     })
    # )
    # captcha = ReCaptchaField() включить в продакшн
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]


class LoginForm(AuthenticationForm):
      username = forms.CharField(max_length=150,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Login')}),
                                   label='')
      password = PasswordEye(label='') # глазок справа в поле ввода - скрыть или показать пароль

      class Meta:
        model = User
        fields = ['username', 'password']

class DocumentForm (forms.ModelForm):
    class Meta:
        model = Documents
        fields = '__all__'
        labels = {
            'title': 'Название документа',
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content',]
        labels = {
            'title': 'Тема сообщения:',
            'content': 'Текст сообщения:'
        }
        widgets = {
            'content': SummernoteWidget(),

        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text'] # Или ['author', 'text'] если автор не заполняется автоматически
        widgets = {
            'text': forms.TextInput(attrs={'class': 'formControl', 'placeholder': 'Ваш комментарий'}),
        }

