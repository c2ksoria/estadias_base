from django.shortcuts import render
# from django.views import generic
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .form import LoginForm

# Create your views here.

class UserLoginView(LoginView):
    template_name= 'registration/login.html'
    form_class = LoginForm
    # success_url= reverse_lazy('home1')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']='Iniciar Sesion'
        return context