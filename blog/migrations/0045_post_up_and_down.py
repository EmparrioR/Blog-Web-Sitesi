# Generated by Django 4.2.3 on 2023-07-26 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0044_alter_comment_text_alter_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='up_and_down',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
