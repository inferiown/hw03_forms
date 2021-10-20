from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Group, Post, User
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'slug': slug,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    user_posts = author.posts.all()
    posts_count = user_posts.count()
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts_count': posts_count,

    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_details.html'
    post = get_object_or_404(Post, pk=post_id)
    username = post.author
    user = get_object_or_404(User, username=username)
    user_posts = user.posts.all()
    posts_count = user_posts.count()
    post_preview = post.text[0:29]
    context = {
        'post': post,
        'posts_count': posts_count,
        'post_preview': post_preview,

    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    error = ''
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('posts:profile', request.user.username)
        else:
            error = 'Форма заполнена неверно'
    form = PostForm()
    context = {
        'form': form,
        'error': error,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    if 'edit' in request.path:
        is_edit = True
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, template, context)
