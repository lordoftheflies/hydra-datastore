from django.conf.urls import url, include
from django.views import generic

from hydra_datastore import views

# Create a router and register our viewsets with it.
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'dataset', views.DatasetViewSet)
router.register(r'entry', views.EntryViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
