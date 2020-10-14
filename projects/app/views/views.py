from django_filters import rest_framework as rest_filters
from rest_framework import (filters, status)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from app.filters import AuctionFilters
from app.models import (Auction, RateMember)
from app.serializers import (ViewAuctionSerializer, ViewRateSerializer, ViewAuctionFinishSerializer)
from app.permissions import (UpdateAuctionPermission, CreateDeleteRatePermission)
from app.utils import get_object_or_404


class AuctionView(ModelViewSet):
    serializer_class = ViewAuctionSerializer
    permission_classes = [IsAuthenticated, UpdateAuctionPermission]
    queryset = Auction.objects.all().order_by('-date_end')
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = AuctionFilters
    filterset_fields = ['date_start', 'date_end']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'date_end']

    def list(self, request, *args, **kwargs):
        if request.GET.get('is_active') == 'true':
            self.queryset = self.queryset.filter(is_active=True)
        else:
            self.queryset = self.queryset.filter(is_active=False)
        queryset_filters = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(queryset_filters)
        if page is not None:
            serializer = self.get_serializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        user = request.user
        data['author'] = user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        model = serializer.create(validated_data=data)
        new_serializer = self.get_serializer(model, context={'request': request})
        return Response(data=new_serializer.data, status=status.HTTP_201_CREATED)


class RateView(ModelViewSet):
    serializer_class = ViewRateSerializer
    permission_classes = [IsAuthenticated, CreateDeleteRatePermission]
    queryset = RateMember.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['member'] = request.user.profile.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        model = serializer.create(validated_data=data)
        new_serializer = self.get_serializer(model, context={'request': request})
        return Response(data=new_serializer.data, status=status.HTTP_201_CREATED)


class AuctionFinishView(ModelViewSet):
    serializer_class = ViewAuctionFinishSerializer
    permission_classes = [IsAuthenticated]
    queryset = Auction.objects.all().order_by('-date_end')

    def retrieve(self, request, pk=None):
        auction = get_object_or_404(
            Auction,
            pk=pk,
            is_active=False,
            error_message='Auction not found or not finished'
        )
        serializer = self.get_serializer(auction)
        return Response(serializer.data, status=status.HTTP_200_OK)
