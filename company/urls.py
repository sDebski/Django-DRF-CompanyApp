from django.urls import path

from rest_framework.routers import SimpleRouter

from company import viewsets, views

router = SimpleRouter()

router.register("labels", viewsets.LabelViewSet, basename="labels")
router.register(
    "projectcategories", viewsets.ProjectCategoryViewSet, basename="projectcategories"
)
router.register("projects", viewsets.ProjectViewSet, basename="projects")

urlpatterns = []
urlpatterns += router.urls
