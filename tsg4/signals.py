from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Entry, BlogPost
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail


@receiver(post_save, sender=User)
def create_notification_for_user(sender, instance, created, **kwargs):
   if created:
       email = instance.email
       name = instance.username
       subject = 'Добро пожаловать на сайт ТСЖ "Царскосёл-4"!'
       message = f'Привет, {name}! \nВы успешно зарегистрировались на сайте "Царскосёл-4".'

       send_mail(
           subject=subject,
           message=message,
           from_email=settings.EMAIL_HOST_USER,
           recipient_list=[email],
           fail_silently=False,
       )


@receiver(post_save, sender=Entry)
def create_notification_for_entry(sender, instance, created, **kwargs):
   if created:
       date = instance.date_created.strftime("%d.%m.%Y")
       domain = '192.168.31.14:8000/notice/'
       full_url = f"http://{domain}"
       users = User.objects.all()
            # Создаем список кортежей для массовой отправки
       email_tuples = []
       for user in users:
               email_tuple = (
                 'Объявление на сайте ТСЖ',  # subject
                    f'Привет, {user.username}! \nПосмотрите новое объявление: \n{full_url}',  # message
                   settings.EMAIL_HOST_USER,  # from_email
                    [user.email],  # recipient_list
                )
               email_tuples.append(email_tuple)
            # Отправляем все письма одним вызовом
       send_mass_mail(email_tuples, fail_silently=False)

@receiver(post_save, sender=BlogPost)
def create_notification_for_post(sender, instance, created, **kwargs):
   if created:
       author = instance.author
       domain = '192.168.31.14:8000/posts/'
       full_url = f"http://{domain}"
       users = User.objects.all()
       email_tuples = []
       for user in users:
               email_tuple = (
                 'Новый пост на сайте ТСЖ',  # subject
                    f'Привет, {user.username}! \nПосмотрите новый пост от {author}: \n{full_url}',  # message
                   settings.EMAIL_HOST_USER,  # from_email
                    [user.email],  # recipient_list
                )
               email_tuples.append(email_tuple)
       send_mass_mail(email_tuples, fail_silently=False)


