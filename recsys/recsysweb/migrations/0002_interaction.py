# Generated by Django 4.1 on 2022-10-10 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recsysweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(db_column='user_id')),
                ('rating', models.FloatField()),
                ('item', models.ForeignKey(db_column='item_id', on_delete=django.db.models.deletion.DO_NOTHING, to='recsysweb.item')),
            ],
        ),
    ]
