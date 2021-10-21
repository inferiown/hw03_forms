from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def make_page_obj(posts, request,
                  page_items_number=settings.DEFAULT_PG_I_NUMBER):
    paginator = Paginator(posts, page_items_number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    page_obj = make_page_obj(post_list, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = make_page_obj(post_list, request)
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
    page_obj = make_page_obj(user_posts, request)
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
    context = {
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    error = ''
    form = PostForm(request.POST or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        form.save()
        return redirect('posts:profile', request.user.username)
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
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'post_id': post_id,
    }
    return render(request, template, context)
