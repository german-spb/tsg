from django.shortcuts import render
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User


def index(request):
    return render(request, 'base.html')

class CustomRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'signup.html'
    extra_context = {'title': 'Регистрация на сайте'}

    def get_success_url(self):
        return reverse_lazy('tsg4:login')

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)
