# Generated by Django 3.2.4 on 2021-06-24 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_review_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='number_of_ratiing',
            field=models.IntegerField(default=0),
        ),
    ]
