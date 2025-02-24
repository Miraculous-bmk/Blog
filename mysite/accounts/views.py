from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseBadRequest
from .form import SignupForm, UserUpdateForm, ProfileUpdateForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:hero')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
@permission_required('accounts.can_update_profile', raise_exception=True)
def profile_update_view(request):
    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'accounts/profile_update.html', context)

def logout_view(request):
    logout(request)
    return redirect('blog:hero')

@login_required
@permission_required('accounts.can_follow_authors', raise_exception=True)
def follow_author(request, author_id):
    """
    Toggle follow state for an author.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")
    author = get_object_or_404(User, pk=author_id)
    profile = request.user.profile
    if author in profile.followed_authors.all():
        profile.followed_authors.remove(author)
    else:
        profile.followed_authors.add(author)
    profile.save()
    return redirect(request.META.get('HTTP_REFERER', 'blog:hero'))
