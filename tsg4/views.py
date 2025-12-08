from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, HttpResponseRedirect, HttpResponseNotFound
from .forms import RegistrationForm, LoginForm, BlogPostForm, CommentForm
from .models import Documents, Entry, BlogPost, Comment
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)



def index(request):
    return render(request, 'base.html')

class CustomRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'signup.html'
    extra_context = {'title': 'Регистрация на сайте'}

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    extra_context = {'title': 'Авторизация на сайте'}

    def get_success_url(self):
        return reverse_lazy('index')

def logout_view(request):
    logout(request)
    return redirect('/')

#================== Открыть документ =============================
def documents(request):
    docs = Documents.objects.all()
    return render(request, 'document.html', {'docs': docs})

@login_required
def document_open(request, filename): #---- вывод изображения PDF документа в браузер
    return FileResponse(open(f'documents/{filename}', 'rb'), content_type='application/pdf')

def useful_information(request):
    return render(request, 'useful_information.html')

#======================= Объявления ============================

def notice(request):
    ads = Entry.objects.all()
    return render(request, 'notice.html', {'ads': ads})

#================ Создание поста ============================

def input_post(request):
    form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})


@login_required
def create_post(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    author = request.user
    post = BlogPost(author= author, title= title, content=content )
    post.save()
    post.instance = None
    return redirect('posts')

def posts(request):
    posts = BlogPost.objects.all().order_by('-date_created')
    return render(request, 'posts.html', {'posts': posts})

def all_posts_user(request):
    posts = BlogPost.objects.filter(author=request.user).order_by('-date_created')
    return render(request, 'all_posts_user.html', {'posts': posts})



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content']
    template_name = 'update_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# class PostDetailView(DetailView):
#     model = BlogPost
#     template_name = 'post_detail.html'

def post_detail( request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user # Предполагаем, что пользователь залогинен
            comment.save()
            return redirect('post-detail', pk=pk)

    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})