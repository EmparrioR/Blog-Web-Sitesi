# Generated by Django 4.2.3 on 2023-07-19 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_comment_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='author2',
        ),
    ]
