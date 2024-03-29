from ..models import RecommenderEnsempleEvaluation, RecommenderEnsempleEvaluationMetric
from singleton_decorator import singleton
from django.db.models import Avg, Count
import math
import statistics
import pandas as pd
from ..logger import get_logger


class Metrics:
    @classmethod
    def idiscount_cumulative_gain(clazz, ratings, descendent=True):
        descendent_ratings = sorted(ratings, reverse=descendent)

        ratings_set = list(set(ratings))
        if len(ratings_set) == 1 and ratings_set[0] <= 2:
            return (8 - ratings_set[0])

        return clazz.discount_cumulative_gain(descendent_ratings)


    @staticmethod
    def discount_cumulative_gain(ratings):
        return sum([float(r) / math.log(i+2, 2) for i, r in enumerate(ratings)])

    @classmethod
    def normalized_discount_cumulative_gain(clazz, ratings, descendent=True):
        return clazz.discount_cumulative_gain(ratings) / clazz.idiscount_cumulative_gain(ratings, descendent)


@singleton
class EvaluationService:
    def __init__(self):
        self.logger = get_logger(self)

    def find_active(self):
        return RecommenderEnsempleEvaluation.objects.filter(enable=True)[0]


    def find_metric_by_active_and_user(self, user):
        evaluation = self.find_active()
        return RecommenderEnsempleEvaluationMetric \
            .objects \
            .filter(evaluation=evaluation, user=user) \
            .order_by('-datetime') [:evaluation.mean_window_size] \
            .aggregate(Avg('value')) \
            .get('value__avg', 0)


    def find_metric_by_active(self):
        evaluation = self.find_active()
        return RecommenderEnsempleEvaluationMetric \
            .objects \
            .filter(evaluation=evaluation) \
            .order_by('-datetime') [:evaluation.mean_window_size] \
            .aggregate(Avg('value')) \
            .get('value__avg', 0)


    def find_metric_values_by_active(self):
        evaluation = self.find_active()
        query = RecommenderEnsempleEvaluationMetric \
            .objects \
            .filter(evaluation=evaluation) \
            .order_by('-datetime') \
            .only('datetime', 'value')

        if query:
            self.logger.info('Query:', query)
            df = pd.DataFrame(list(map(lambda it: {'datetime': it.datetime, 'value': it.value}, query)))
            df['datetime'] = pd.to_datetime(df['datetime'])
        else:
            df = pd.DataFrame()

        return df

    def find_metric_values_by_active_and_user(self, user):
        evaluation = self.find_active()
        query = RecommenderEnsempleEvaluationMetric \
            .objects \
            .filter(evaluation=evaluation, user=user) \
            .order_by('-datetime') \
            .only('datetime', 'value')

        if query:
            df=  pd.DataFrame(list(map(lambda it: {'datetime': it.datetime, 'value': it.value}, query)))
            df['datetime'] = pd.to_datetime(df['datetime'])
        else:
            df = pd.DataFrame()

        return df


    def user_votes_by_active(self):
        evaluation = self.find_active()

        query = list(RecommenderEnsempleEvaluationMetric.objects \
            .filter(evaluation=evaluation) \
            .values('user__username') \
            .annotate(total=Count('value')) \
            .values('user__username', 'total'))

        return pd.DataFrame(query)


    def evaluate_session(self, user, items_rating):
        discount_cumulative_gain = Metrics.normalized_discount_cumulative_gain(items_rating.values())

        evaluation = self.find_active()

        mertic = RecommenderEnsempleEvaluationMetric(
            evaluation = evaluation,
            user       = user,
            value      = discount_cumulative_gain
        )
        mertic.save()

    def remove_metrics_by_user(self, user):
        RecommenderEnsempleEvaluationMetric.objects.filter(user=user).delete()
