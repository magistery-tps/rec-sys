# Generated by Django 4.1 on 2022-12-29 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recsysweb', '0031_alter_recommender_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recommender',
            options={'permissions': (('info', 'Show recommender debug information'),)},
        ),
    ]
