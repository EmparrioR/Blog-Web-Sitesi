# Generated by Django 4.2.3 on 2023-07-26 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0045_post_up_and_down'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='up_and_down',
            field=models.IntegerField(default=0),
        ),
    ]