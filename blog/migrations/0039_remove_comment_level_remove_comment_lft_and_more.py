# Generated by Django 4.2.3 on 2023-07-24 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0038_alter_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='level',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='tree_id',
        ),
    ]
