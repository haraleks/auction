from collections import OrderedDict

import math
from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class PageNumberPagination(LimitOffsetPagination):

    def get_paginated_response(self, data):
        meta_dict = {
            'count_page': math.ceil(self.count / settings.REST_FRAMEWORK['PAGE_SIZE']),
            'count_items': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        }
        return Response(OrderedDict([
             ('_meta', meta_dict),
             ('result', data)
        ]))
