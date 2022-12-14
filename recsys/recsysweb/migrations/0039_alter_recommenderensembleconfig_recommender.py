# Generated by Django 4.1 on 2023-01-07 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recsysweb', '0038_alter_recommender_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommenderensembleconfig',
            name='recommender',
            field=models.ForeignKey(db_column='recommender_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_recommender_id', to='recsysweb.recommender', verbose_name='Recommender'),
        ),
    ]
