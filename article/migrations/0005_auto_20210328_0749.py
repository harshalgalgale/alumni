# Generated by Django 3.1.7 on 2021-03-28 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20210325_0037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='member',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='image',
            new_name='feature_image',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='headline',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='member',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='image',
            new_name='feature_image',
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='headline',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='bulletin',
            old_name='member',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='bulletin',
            old_name='image',
            new_name='feature_image',
        ),
        migrations.RenameField(
            model_name='bulletin',
            old_name='headline',
            new_name='title',
        ),
    ]
