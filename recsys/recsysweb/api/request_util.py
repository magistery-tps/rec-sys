from django.contrib.auth.models import User
from ..models import Item
from rest_framework import status
from rest_framework.response import Response


class RequestUtl:
    @staticmethod
    def getUser(id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                data={
                    'code': 'NOT_FOUND_USER',
                    'message': f'No found a user with {id} id.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @staticmethod
    def getItem(id):
        try:
            return Item.objects.get(id=id)
        except Item.DoesNotExist:
            return Response(
                data={
                    'code': 'NOT_FOUND_ITEM',
                    'message': f'No found a item with {user_id} id.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @staticmethod
    def getRecommender(ctx, id):
        try:
            return ctx.recommender_service.find_by_id(id)
        except:
            return Response(
                data={
                    'code': 'NOT_FOUND_RECOMMENDER',
                    'message': f'Not found a recommender with {id} id.'
                },
                status=status.HTTP_404_NOT_FOUND
            )