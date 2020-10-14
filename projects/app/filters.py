from datetime import datetime

from django_filters import rest_framework as rest_filters

from app.models import Auction


class AuctionFilters(rest_filters.FilterSet):
    date_start = rest_filters.CharFilter(method='search_date_start')
    date_end = rest_filters.CharFilter(method='search_date_end')
    create_at = rest_filters.CharFilter(method='search_date_create')

    class Meta:
        model = Auction
        exclude = ['logo', 'comment', 'widget_link']

    def search_date_start(self, queryset, name, value):
        datetime_object = datetime.strptime(value, '%Y-%m-%d')
        return queryset.filter(date_start__date=datetime_object)

    def search_date_end(self, queryset, name, value):
        datetime_object = datetime.strptime(value, '%Y-%m-%d')
        return queryset.filter(date_end__date=datetime_object)

    def search_date_create(self, queryset, name, value):
        datetime_object = datetime.strptime(value, '%Y-%m-%d')
        return queryset.filter(create_at__date=datetime_object)
