"""
URL configuration for TSG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from tsg4 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup/', views.CustomRegistrationView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('document/', views.documents),
    path('documents/<str:filename>/', views.document_open),
    path('useful_information/', views.useful_information),
    path('notice/', views.notice),
    path('froala_editor/', include('froala_editor.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('input_post/create_post/', views.create_post),
    path('input_post/', views.input_post, name='add_post'),
    path('posts/', views.posts, name='posts'),
    path('posts_user/', views.all_posts_user, name='posts_user'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(success_url="/posts/"), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    ]
