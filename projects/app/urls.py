from django.urls import path

from app.views import (UserProfileView, AuctionView, RateView, AuctionFinishView)

as_view_common = {
    'get': 'list',
    'post': 'create',
}

as_view_with_pk = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
}

as_view_without_put_pk = {
    'get': 'retrieve',
    'delete': 'destroy'
}

urlpatterns = [
    path('profiles/', UserProfileView.as_view(as_view_common), name='profiles'),
    path('profiles/<int:pk>/', UserProfileView.as_view(as_view_with_pk), name='profiles_pk'),
    path('auction/', AuctionView.as_view(as_view_common), name='auction'),
    path('auction/<int:pk>/', AuctionView.as_view(as_view_with_pk), name='auction_pk'),
    path('auction/finish/<int:pk>/', AuctionFinishView.as_view({'get': 'retrieve'}), name='auction_finish_pk'),
    path('rate/', RateView.as_view(as_view_common), name='rate'),
    path('rate/<int:pk>/', RateView.as_view(as_view_without_put_pk), name='rate_pk'),
]
