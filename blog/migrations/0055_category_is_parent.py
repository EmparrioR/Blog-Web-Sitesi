# Generated by Django 4.2.3 on 2023-08-07 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0054_alter_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_parent',
            field=models.BooleanField(default=False),
        ),
    ]
