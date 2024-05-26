from django.shortcuts import redirect, render

from blogs.models import Blog, Category

from assignments.models import About


# from .forms import RegistrationForm
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib import auth


def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False, status='Published')
    # Fetch about us
    try:
        about = About.objects.get()
    except:
        about = None
    context = {
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about,
    }
    return render(request, 'home.html', context)
