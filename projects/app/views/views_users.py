from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.generics import (ListAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models import UserProfile
from app.serializers import UserProfileSerializer, UserValidateSerializer
from app.utils import get_object_or_404

User = get_user_model()


class UserProfileView(viewsets.GenericViewSet, ListAPIView):
    """ View CRUD method User profile """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """ registered clients"""
        serializer = UserValidateSerializer(data=request.data)
        serializer.validate_password(value=request.data['password2'])
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.data)
        use_profile = UserProfile.objects.create(user=user)
        data_response = self.get_serializer(use_profile).data
        return Response(data=data_response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(
            self.get_queryset(), pk=pk, error_message='Пользователь не найден!'
        )
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        profile = get_object_or_404(self.get_queryset(),
                                    pk=pk,
                                    error_message='Profile User not found')
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        new_serializer = self.get_serializer(
            instance, context={'request': request}
        )
        return Response(new_serializer.data)

    def destroy(self, request, pk=None):
        client_profile = get_object_or_404(
            self.get_queryset(), pk=pk, error_message='Пользователь не найден!'
        )
        user_id = client_profile.user.id
        client_profile.delete()
        user = get_object_or_404(
            User, pk=user_id, error_message='Пользователь не найден!'
        )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
