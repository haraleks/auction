from datetime import datetime

import pytz
from django.shortcuts import _get_queryset as get_queryset
from rest_framework.exceptions import NotFound


def get_object_or_404(klass, error_message='Object does not exist', *args, **kwargs):
    queryset = get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise NotFound(detail={'detail': error_message})


def update_date_timzone(date, format='%Y-%m-%d %H:%M:%S'):
    unaware_start_date = datetime.strptime(date, format)
    return pytz.utc.localize(unaware_start_date)
