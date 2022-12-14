# Generated by Django 4.1 on 2023-01-08 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recsysweb', '0046_alter_recommenderensembleconfig_ensemble'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommenderEnsempleEvaluation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
                ('ensemble', models.ForeignKey(db_column='ensemble_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_ensemble_id', to='recsysweb.recommenderensemble', verbose_name='Recommender Ensemble')),
            ],
        ),
        migrations.CreateModel(
            name='RecommenderEnsempleEvaluationMetric',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.FloatField()),
                ('evaluation', models.ForeignKey(db_column='evaluation_id', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_evaluation_id', to='recsysweb.recommenderensempleevaluation', verbose_name='Recommender Ensemble Evaluation')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_user_id', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.AddIndex(
            model_name='recommenderensempleevaluationmetric',
            index=models.Index(fields=['evaluation', 'user'], name='recsysweb_r_evaluat_481430_idx'),
        ),
        migrations.AddIndex(
            model_name='recommenderensempleevaluationmetric',
            index=models.Index(fields=['evaluation'], name='recsysweb_r_evaluat_723826_idx'),
        ),
        migrations.AddIndex(
            model_name='recommenderensempleevaluationmetric',
            index=models.Index(fields=['user'], name='recsysweb_r_user_id_7b8772_idx'),
        ),
        migrations.AddIndex(
            model_name='recommenderensempleevaluation',
            index=models.Index(fields=['enable', 'ensemble'], name='recsysweb_r_enable_00558a_idx'),
        ),
    ]
