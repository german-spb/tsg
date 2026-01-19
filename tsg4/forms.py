from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

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
        label='Имя / Ник / Квартира-...',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
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

    password2 = PasswordEye(label='')

    # captcha = ReCaptchaField() включить в продакшн

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]



class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('Login')}),
                               label='')
    password = PasswordEye(label='')

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

#======================= Сброс пароля ============================

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите ваш Email',
                   "autocomplete": "email"}
        )
    )


class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": "Пароли не совпадают"
    }
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите новый пароль',
                   "autocomplete": "new-password"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Подтвердите новый пароль',
                   "autocomplete": "new-password"}
        ),
    )