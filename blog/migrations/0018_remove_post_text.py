# Generated by Django 4.2.3 on 2023-07-19 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_post_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
    ]
