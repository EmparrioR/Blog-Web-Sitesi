# Generated by Django 4.2.3 on 2023-08-07 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0055_category_is_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_parent',
        ),
    ]
