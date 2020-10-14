from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from app.models import (UserProfile, Auction, RateMember)
from app.utils import update_date_timzone

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """Create and show user profile"""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class UserValidateSerializer(serializers.Serializer):
    """validate user data"""
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except Exception as e:
            raise NotFound(detail={'detail': e})
        return value


class ViewAuctionSerializer(serializers.ModelSerializer):
    """Create and show auction"""
    last_rate = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.SerializerMethodField()
    date_start = serializers.DateTimeField()
    date_end = serializers.DateTimeField()

    class Meta:
        model = Auction
        fields = ['id', 'name', 'description', 'rate_start', 'last_rate',
                  'date_start', 'date_end', 'is_active', 'author']

    def get_last_rate(self, instance):
        """ Return last rate """
        auction_rate = RateMember.objects.filter(auction=instance).order_by('-created_at')
        last_rate = auction_rate.first()
        if last_rate is None:
            return None
        return last_rate.rate

    def get_is_active(self, instance):
        """ Check auction on finised"""
        return instance.check_finish()

    def create(self, validated_data):
        author_id = validated_data.pop('author')
        validated_data['date_start'] = update_date_timzone(validated_data.pop('date_start'))
        validated_data['date_end'] = update_date_timzone(validated_data.pop('date_end'))
        author = User.objects.get(pk=author_id)
        auction = Auction.objects.create(**validated_data)
        auction.author = author
        auction.save()
        return auction


class ViewAuctionFinishSerializer(serializers.ModelSerializer):
    """Show auction finished"""
    last_rate = serializers.SerializerMethodField()
    name_win = serializers.SerializerMethodField()
    email_win = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ['id', 'name', 'description', 'last_rate',
                  'date_start', 'date_end', 'is_active',
                  'name_win', 'email_win']

    def get_last_rate(self, instance):
        auction_rate = RateMember.objects.filter(auction=instance).order_by('-created_at')
        last_rate = auction_rate.first()
        if last_rate is None:
            return None
        return last_rate.rate

    def get_name_win(self, instance):
        auction_rate = RateMember.objects.filter(auction=instance).order_by('-created_at')
        last_rate = auction_rate.first()
        if last_rate is None:
            return None
        return last_rate.member.name

    def get_email_win(self, instance):
        auction_rate = RateMember.objects.filter(auction=instance).order_by('-created_at')
        last_rate = auction_rate.first()
        if last_rate is None:
            return None
        return last_rate.member.user.email

    def get_is_active(self, instance):
        return instance.check_finish()


class ViewRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RateMember
        fields = '__all__'

    def validate(self, attrs):
        date_now = datetime.now() + timedelta(seconds=3)
        date_end = attrs['auction'].date_end.replace(tzinfo=None)
        if date_now.replace(tzinfo=None) >= date_end:
            raise serializers.ValidationError({'error': ['Auction is over']})
        last_rate = RateMember.objects.filter(auction=attrs['auction'].pk).last()
        if attrs['rate'] <= attrs['auction'].rate_start or attrs['rate'] <= last_rate.rate:
            raise serializers.ValidationError({'error': ['Rate is the same or less than the starting rate.']})
        return attrs

    def create(self, validated_data):
        auction = Auction.objects.get(pk=validated_data.pop('auction'))
        user_profile = UserProfile.objects.get(pk=validated_data.pop('member'))
        date_delta = auction.date_end - timezone.now()
        if date_delta.seconds < 60:
            auction.date_end = auction.date_end + timedelta(minutes=2)
            auction.save()
        model = RateMember.objects.create(**validated_data)
        model.member = user_profile
        model.auction = auction
        model.save()
        return model
