from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import User
from blog.models import Post  # Your blog app’s Post model
from .forms import AuthorSignupForm, AuthorProfileForm

import datetime
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from blog.models import Post

def is_author(user):
    """Check if the user has an associated AuthorProfile."""
    return hasattr(user, 'author_profile')

def author_signup(request):
    if request.method == 'POST':
        form = AuthorSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create an empty AuthorProfile for the new author
            user.author_profile = user.author_profile if hasattr(user, 'author_profile') else None
            if not user.author_profile:
                from .models import AuthorProfile
                AuthorProfile.objects.create(user=user)
            login(request, user)
            return redirect('authors:dashboard')
    else:
        form = AuthorSignupForm()
    return render(request, 'authors/signup.html', {'form': form})

@login_required
@user_passes_test(is_author)
def dashboard(request):
    """Author dashboard displaying a list of their posts."""
    posts = Post.objects.filter(author=request.user)
    return render(request, 'authors/dashboard.html', {'posts': posts})

@login_required
@user_passes_test(is_author)
def profile_view(request):
    profile = request.user.author_profile
    return render(request, 'authors/profile.html', {'profile': profile})

@login_required
@user_passes_test(is_author)
def profile_update(request):
    profile = request.user.author_profile
    if request.method == 'POST':
        form = AuthorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('authors:profile')
    else:
        form = AuthorProfileForm(instance=profile)
    return render(request, 'authors/profile_update.html', {'form': form})

@login_required
@user_passes_test(is_author)
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        category = request.POST.get('category')  # Ensure this is one of your valid choices
        image = request.FILES.get('image')
        
        # Create a unique slug. In production, you'd need to handle slug conflicts.
        slug = slugify(title)
        
        post = Post.objects.create(
            title=title,
            body=body,
            slug=slug,
            category=category,
            author=request.user,
            image=image,
            status=Post.Status.PUBLISHED,
            publish=datetime.datetime.now()
        )
        return redirect('authors:dashboard')
    return render(request, 'authors/create_post.html')

@login_required
@user_passes_test(is_author)
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.body = request.POST.get('body')
        post.category = request.POST.get('category')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        # Optionally, update slug if the title has changed:
        post.slug = slugify(post.title)
        post.save()
        return redirect('authors:dashboard')
    return render(request, 'authors/edit_post.html', {'post': post})

@login_required
@user_passes_test(is_author)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('authors:dashboard')
    return render(request, 'authors/delete_post.html', {'post': post})