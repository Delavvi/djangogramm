# Generated by Django 5.0.3 on 2024-04-23 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_alter_feedphotos_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedphotos',
            name='small_photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/feeds'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='small_photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/feeds'),
        ),
    ]
