from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('game/create/login', views.login),
    path('game/create', views.create),
    path('game/join', views.join),
    path(r'game/id', views.id),
]