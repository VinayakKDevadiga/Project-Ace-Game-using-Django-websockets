from django.urls import path
from .views import *

urlpatterns=[
    path('',home,name="home1"),
    path('index/',index, name='index1'),
    path('game/',game, name='game1'),
    path('<str:error>/',home, name='gameerror1'),
]
