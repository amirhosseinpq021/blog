from django.shortcuts import redirect, render

# from blogs.models import Blog, Category
# from assignments.models import About
# from .forms import RegistrationForm
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib import auth


def home(request):
    return render(request, 'home.html',)