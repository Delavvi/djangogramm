# Generated by Django 5.0.3 on 2024-03-29 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_grampost_tags_alter_photos_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to='media/avatar'),
        ),
    ]
