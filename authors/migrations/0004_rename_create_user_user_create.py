# Generated by Django 4.2 on 2023-04-21 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0003_user_create_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='create_user',
            new_name='create',
        ),
    ]