from collections.abc import Iterable
import json

from django.http import JsonResponse
from django.core.serializers import serialize


def get_json(objs):
    if not issubclass(type(objs), Iterable):
        objs = [objs]

    serialized_data = serialize("json",  objs, use_natural_foreign_keys=True)
    serialized_data = json.loads(serialized_data)
    return JsonResponse(serialized_data, status=200, safe=False)
