from django.urls import path
from .import views

urlpatterns = [ 
    path('', views.home, name='home'),
    path('recommendations', views.recommendations, name='recommendations'),
    path('likes', views.likes, name='likes')
]
