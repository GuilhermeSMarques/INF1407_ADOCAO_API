from rest_framework.routers import DefaultRouter

from .views import SolicitacaoAdocaoViewSet

router = DefaultRouter()
router.register('', SolicitacaoAdocaoViewSet, basename='solicitacao-adocao')

urlpatterns = router.urls