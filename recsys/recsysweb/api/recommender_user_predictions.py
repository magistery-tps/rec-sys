from .request_util import RequestUtl
from rest_framework import serializers, viewsets
from ..models import SimilarityMatrix, SimilarityMatrixCell
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..logger import get_logger
from ..models import Recommendations, Recommender
from ..recommender import RecommenderCapability, RecommenderContext

# Domain
from ..domain                       import DomainContext

ctx = DomainContext()


from rest_framework import serializers



class RecommenderMetadataSerializer(serializers.Serializer):
    id          = serializers.IntegerField()
    title       = serializers.CharField()
    features    = serializers.CharField()
    description = serializers.CharField()

class RecommendationItemSerializer(serializers.Serializer):
    id          = serializers.IntegerField()
    name        = serializers.CharField()
    description = serializers.CharField()
    popularity  = serializers.FloatField()
    rating      = serializers.FloatField()
    votes       = serializers.IntegerField()

class RecommendationsSerializer(serializers.Serializer):
    recommender    = RecommenderMetadataSerializer(source='metadata')
    info        = serializers.CharField()
    items       =  RecommendationItemSerializer(many=True)


class RecommenderUserPredictionsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated]

    def get(self, request, recommender_id=None, user_id=None):
        user        = RequestUtl.getUser(user_id)
        recommender = RequestUtl.getRecommender(ctx, recommender_id)

        rec_ctx         = RecommenderContext(user=user)
        recommendations = recommender.recommend(rec_ctx)

        serializer = RecommendationsSerializer(recommendations)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
