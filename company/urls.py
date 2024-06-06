from django.urls import path

from rest_framework.routers import SimpleRouter

from company import viewsets, views

router = SimpleRouter()

router.register("labels", viewsets.LabelViewSet, basename="labels")
router.register(
    "projectcategories", viewsets.ProjectCategoryViewSet, basename="projectcategories"
)
router.register("projects", viewsets.ProjectViewSet, basename="projects")
router.register("workers", viewsets.WorkerViewSet, basename="workers")
router.register("tasks", viewsets.TaskViewSet, basename="tasks")

urlpatterns = [
    path("cache/", views.CachedView.as_view(), name="cache"),
    path("rpc_order/", views.RPCTaskSetView.as_view(), name="rpc_order"),
    path("rpc_result/<str:task_id>/", views.RPCTaskResultView.as_view(), name="rpc_result"),
]
urlpatterns += router.urls
