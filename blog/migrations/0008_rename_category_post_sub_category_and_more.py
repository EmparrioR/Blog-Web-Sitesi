# Generated by Django 4.2.3 on 2023-07-18 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_rename_subcategory_post_parent_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='category',
            new_name='sub_category',
        ),
        migrations.RemoveField(
            model_name='post',
            name='parent_category',
        ),
    ]
