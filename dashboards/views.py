from django.shortcuts import render, redirect
from blogs.models import Category, Blog

from django.contrib.auth.decorators import login_required

from .forms import CategoryForm, BlogPostsForm

from django.shortcuts import get_object_or_404

from django.template.defaultfilters import slugify

from django.contrib.auth.models import User

from .forms import AddUserForm, EditUserForm


# Create your views here.


@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


def categories(request):
    return render(request, 'dashboard/categories.html')


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_category.html', context)


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'dashboard/edit_category.html', context)


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')


# __________________________________________________________________________________________________

# blog post crud views

# view posts == R
def posts(request):
    post = Blog.objects.all()
    context = {
        'post': post,
    }
    return render(request, 'dashboard/posts.html', context)


# Add posts == C
def add_post(request):
    if request.method == 'POST':
        form = BlogPostsForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # temporarily saving the form
            post.author = request.user
            post.save()

            # unique slug
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
    else:
        form = BlogPostsForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_post.html', context)


def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogPostsForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
    form = BlogPostsForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'dashboard/edit_posts.html', context)


def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')


# ____________________________________________________________________________________________________________________

# read
def users(request):
    all_users = User.objects.all()
    context = {
        'users': all_users,
    }
    return render(request, 'dashboard/users.html', context)


# creat
def add_user(request, form=None):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddUserForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_user.html', context)


# update
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EditUserForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/edit_user.html', context)


# delete
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('dashboard')
