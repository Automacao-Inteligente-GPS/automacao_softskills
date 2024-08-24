from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()
router.register('autoavaliacao_notas', AutoavaliacaoViewSet, basename='Autoavaliação Nota')
router.register('discentes', DiscenteViewSet, basename='Discentes')

urlpatterns = [
    path('', include(router.urls)),
    path('discentes_notas/<int:id>/', DiscenteDetailView.as_view(), name='discente-detail'),
    path('delete-all-records/', DeleteAllRecordsAPIView.as_view(), name='delete-all-records'),
]
