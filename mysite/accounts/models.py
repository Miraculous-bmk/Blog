from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    social_link = models.URLField(blank=True, null=True)
    followed_authors = models.ManyToManyField(
        User, 
        related_name="followers", 
        blank=True,
        help_text="Select authors to follow"
    )

    class Meta:
        permissions = [
            ("can_comment", "Can comment on posts"),
            ("can_share", "Can share posts"),
            ("can_send_article", "Can send article via email"),
            ("can_update_profile", "Can update profile"),
            ("can_follow_authors", "Can follow authors"),
        ]

    def __str__(self):
        return f"{self.user.username} Profile"
