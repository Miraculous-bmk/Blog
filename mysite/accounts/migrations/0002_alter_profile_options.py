# Generated by Django 5.1.6 on 2025-02-23 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={
                "permissions": [
                    ("can_comment", "Can comment on posts"),
                    ("can_share", "Can share posts"),
                    ("can_send_article", "Can send article via email"),
                    ("can_update_profile", "Can update profile"),
                    ("can_follow_authors", "Can follow authors"),
                ]
            },
        ),
    ]
