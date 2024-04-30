from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()
router.register('autoavaliacao_notas', AutoavaliacaoViewSet, basename='Autoavaliação Nota')

urlpatterns = [
    path('', include(router.urls)),
]