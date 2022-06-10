from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import logging

log = logging.getLogger(__name__)

from .services import datasource
from .grafana_json_datasource import (
    PayloadInvalidError,
    ScopeDoesNotExistError,
    ProjectDoesNotExistError,
    TagValuesKeyMissingError,
    CallbackDoesNotExistError,
    MetricsDataKeyMissingError,
    TagValuesInvalidValueError,
    MetricsQueryKeyMissingError,
    MetricsDataInvalidValueError,
    MetricsQueryInvalidValueError,
)


@csrf_exempt
def index(_):
    return HttpResponse(status=200)


@csrf_exempt
def search(_):
    return JsonResponse(datasource.search(), safe=False)


@csrf_exempt
def query(request):
    if body := request.body.decode("utf-8"):
        try:
            data = json.loads(body)
        except ValueError as err:
            return HttpResponse(err, status=400)

        try:
            result = datasource.query(data)
            return JsonResponse(result, safe=False)

        except (
            ScopeDoesNotExistError,
            MetricsDataKeyMissingError,
            MetricsDataInvalidValueError,
            MetricsQueryKeyMissingError,
            MetricsQueryInvalidValueError,
            TagValuesKeyMissingError,
            TagValuesInvalidValueError,
            CallbackDoesNotExistError,
            PayloadInvalidError,
            ProjectDoesNotExistError,
        ) as err:
            log.warning(f"Datasource query returned {err.message}.")
            return HttpResponse(err.message, status=400)

    return JsonResponse([], safe=False)


@csrf_exempt
def variable(request):
    if body := request.body.decode("utf-8"):
        data = json.loads(body)
        return JsonResponse(datasource.variable(data), safe=False)
    else:
        log.info("No variables found, returning empty response.")
        return JsonResponse([], safe=False)
