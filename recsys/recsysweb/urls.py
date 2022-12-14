from django.urls import path, include
from rest_framework import routers, viewsets
from .import views
from .api import    (
                        InteractionViewSet,
                        ItemViewSet,
                        SimilarityMatrixViewSet,
                        SimilarityMatrixCellViewSet,
                        UserViewSet,
                        RecommenderViewSet,
                    )


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)
router.register(r'interactions', InteractionViewSet)
router.register(r'similarity-matrix', SimilarityMatrixViewSet)
router.register(r'similarity-matrix-cells', SimilarityMatrixCellViewSet)
router.register(r'recommenders', RecommenderViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-in',  views.sign_in,  name='sign-in' ),
    path('sign-out', views.sign_out, name='sign-out'),

    path('recommendations', views.recommendations, name='recommendations'),
    path('likes',           views.likes,           name='likes'),

    path('items',                                       views.list_items,   name='items'),
    path('items/create',                                views.create_item,  name='items.create'),
    path('items/edit/<int:id>/items',                   views.edit_item,    name='items.edit'),
    path('items/edit/<int:id>/<str:origin>/',           views.edit_item,    name='items.edit'),
    path('items/detail/<int:id>/<int:recommender_id>',  views.detail_item,  name='items.detail'),
    path('items/remove/<int:id>',                       views.remove_item,  name='items.remove'),
    path('interactions/remove-all/',                    views.remove_all,   name='interactions.remove_all'),

    path('api/', include(router.urls)),
]
