# Generated by Django 4.2.3 on 2023-07-24 09:35

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0035_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
    ]