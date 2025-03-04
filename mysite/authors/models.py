from django.db import models
from django.contrib.auth.models import User

class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='authors/', blank=True, null=True)
    social_link = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
