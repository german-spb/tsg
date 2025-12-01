from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, HttpResponseRedirect, HttpResponseNotFound
from .forms import RegistrationForm, LoginForm, BlogPostForm
from .models import Documents, Entry, BlogPost
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



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
@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace with your url name
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})

def posts(request):
    posts = BlogPost.objects.all()
    return render(request, 'posts.html', {'posts': posts})
