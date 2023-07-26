# Generated by Django 4.2.3 on 2023-07-26 14:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0048_post_down_post_up'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='voters',
            field=models.ManyToManyField(blank=True, related_name='voted_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]