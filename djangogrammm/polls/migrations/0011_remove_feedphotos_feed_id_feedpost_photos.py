# Generated by Django 5.0.3 on 2024-04-12 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_feedpost_feedphotos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedphotos',
            name='feed_id',
        ),
        migrations.AddField(
            model_name='feedpost',
            name='photos',
            field=models.ManyToManyField(related_name='photos', to='polls.feedphotos'),
        ),
    ]