# Generated by Django 5.1.4 on 2025-01-09 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_post_mainphoto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content',
            new_name='contents',
        ),
    ]
