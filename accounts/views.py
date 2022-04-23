from django.shortcuts import render

# Create your views here.
from django.views import generic
from .forms import CustomUserCreation
from django.urls import reverse_lazy


class SignUpView(generic.CreateView):
    form_class = CustomUserCreation
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
