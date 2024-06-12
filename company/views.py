from django.shortcuts import render
from rest_framework import generics, response, status
from drf_spectacular.utils import OpenApiParameter, extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from django.conf import settings
from company.utils import calculate_value
from company.tasks import test_add

from celery.result import AsyncResult

class CachedView(generics.GenericAPIView):
    """
    View imitating long-drawn task with aching based on value
    """

    permission_classes = []

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="value",
                type=str,
                location=OpenApiParameter.QUERY,
            )
        ]
    )
    @method_decorator(cache_page(60 * settings.CACHE_TIMEOUT_MIN))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, requset):
        value = requset.query_params.get("value")
        calculated_value = calculate_value(value=value)
        data = {"value": calculated_value, "message": "Cached message"}
        return response.Response(data=data, status=status.HTTP_200_OK)


class RPCTaskSetView(generics.GenericAPIView):
    permission_classes = []

    def get(self, requset):
        test_add.delay(10,20)
        data = {"message": "RPC result successfully ordered."}
        return response.Response(data=data, status=status.HTTP_200_OK)
    

class RPCTaskResultView(generics.GenericAPIView):
    permission_classes = []

    def get(self, request, task_id, *args, **kwargs):
        task_result = AsyncResult(task_id)
        if task_result.ready():
            result = task_result.result
        else:
            result = 'Task is still processing'
        return response.Response({'task_id': task_id, 'result': result})