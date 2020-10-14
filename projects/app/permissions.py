from rest_framework.permissions import (BasePermission, SAFE_METHODS)


class IsOwnerProfileOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class UpdateAuctionPermission(BasePermission):
    """ permission for superuser and author"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method == 'PUT':
            if obj.author == request.user:
                return True
        return False


class CreateDeleteRatePermission(BasePermission):
    """ permission for superuser and author"""

    def has_object_permission(self, request, view, obj):
        method_allow = ['POST', 'DELETE']
        if request.user.is_superuser:
            return True
        if request.method in method_allow:
            if request.user.profile.is_client:
                return True
        return False
