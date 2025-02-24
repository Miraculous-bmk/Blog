from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import follow_author

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('follow/<int:author_id>/', follow_author, name='follow_author'),
]