# Generated by Django 4.2.3 on 2023-07-24 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0042_comment_level_comment_lft_comment_rght_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='level',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]
