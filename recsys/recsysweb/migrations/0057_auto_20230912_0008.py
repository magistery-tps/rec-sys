# Generated by Django 4.1 on 2023-09-12 00:08

from django.db import migrations, models
import django.utils.timezone


def set_created_at_default(apps, schema_editor):
    Interaction = apps.get_model('recsysweb', 'Interaction')
    Interaction.objects.filter(created_at=None).update(created_at=django.utils.timezone.now())


class Migration(migrations.Migration):

    dependencies = [
        ('recsysweb', '0056_alter_recommender_max_items_by_similar_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.RunPython(set_created_at_default),
    ]