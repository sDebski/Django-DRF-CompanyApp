from django.urls import path

from rest_framework.routers import SimpleRouter

from company import viewsets, views

router = SimpleRouter()

router.register("labels", viewsets.LabelViewset, basename="labels")

urlpatterns = []
urlpatterns += router.urls
