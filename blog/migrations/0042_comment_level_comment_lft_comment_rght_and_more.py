# Generated by Django 4.2.3 on 2023-07-24 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0041_remove_reply_parent_comment_reply_parent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='level',
            field=models.PositiveIntegerField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, editable=False, null=True),
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]