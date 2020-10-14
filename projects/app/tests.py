from django.contrib.auth import get_user_model
from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import (APITestCase, URLPatternsTestCase, APIClient)
from rest_framework_simplejwt.tokens import AccessToken

from app.models import (UserProfile, Auction, RateMember)
from app.utils import update_date_timzone

from django.conf import settings
SIMPLE_JWT = settings.SIMPLE_JWT


class InitClass(APITestCase, URLPatternsTestCase):
    User = get_user_model()

    urlpatterns = [
        path('api/v1/', include('auction.urls')),
    ]

    def create_user(self):
        user = self.User.objects.create(username='TestUser',
                                        # email='testuser@gmail.com',
                                        password='PaSwOrD123',
                                        is_active=True)
        profile = UserProfile.objects.create(user=user,
                                             name='Test')
        access = AccessToken.for_user(user)
        client = self.login_user(access)
        return user, client, profile

    @staticmethod
    def login_user(token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=SIMPLE_JWT['AUTH_HEADER_TYPES'][0] +
                                              ' ' + str(token))  # simulate logged-in user
        return client


class ProfileTestCase(InitClass):
    def setUp(self):
        self.user, self.client, self.profile = self.create_user()
        self.path_pk = reverse('profiles_pk', args=[self.profile.pk])

    def test_get(self):
        response = self.client.get(reverse('profiles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        data = {
            "username": "Test2",
            "email": "test2@test.do",
            "password": "pAssw!1234",
            "password2": "pAssw!1234"
        }
        response = self.client.post(reverse('profiles'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        data = {
            "name": "Test3",
        }
        response = self.client.put(self.path_pk, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_delete(self):
        response = self.client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AuctionTestCase(InitClass):
    def setUp(self):
        self.user, self.client, self.profile = self.create_user()
        self.auction, _ = Auction.objects.get_or_create(name='New Auction',
                                                     description='Description big',
                                                     date_start=update_date_timzone('2020-10-11', '%Y-%m-%d'),
                                                     date_end=update_date_timzone('2020-11-11', '%Y-%m-%d'),
                                                     rate_start='1000',
                                                     author=self.user)
        self.path_pk = reverse('auction_pk', args=[self.auction.pk])

    def test_get(self):
        response = self.client.get(reverse('auction'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        data = {
            "name": 'New Auction2',
            "description": 'Description big new',
            "date_start": '2020-10-12 10:00:00',
            "date_end": '2020-10-13 10:00:00',
            "rate_start": '2000',
        }
        response = self.client.post(reverse('auction'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        data = {
            "name": 'Auction2',
            "description": 'Description new',
            "date_start": '2020-10-12 10:00:00',
            "date_end": '2020-10-13 10:00:00',
            "rate_start": '2500'
        }
        response = self.client.put(self.path_pk, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_delete(self):
        response = self.client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RateTestCase(InitClass):
    def setUp(self):
        self.user, self.client, self.profile = self.create_user()
        self.auction, _ = Auction.objects.get_or_create(name='New Auction',
                                                     description='Description big',
                                                     date_start=update_date_timzone('2020-10-11', '%Y-%m-%d'),
                                                     date_end=update_date_timzone('2020-11-11', '%Y-%m-%d'),
                                                     rate_start='1000',
                                                     author=self.user)
        self.rate, _ = RateMember.objects.get_or_create(member=self.profile,
                                                        auction=self.auction,
                                                        rate=1000)
        self.path_pk = reverse('rate_pk', args=[self.rate.pk])

    def test_get(self):
        response = self.client.get(reverse('rate'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        data = {
            "member": self.profile.pk,
            "auction": self.auction.pk,
            "rate": '2500',
        }
        response = self.client.post(reverse('rate'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self):
        data = {
            "rate": '3000',
        }
        response = self.client.put(self.path_pk, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        response = self.client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AuctionFinishTestCase(InitClass):
    def setUp(self):
        self.user, self.client, self.profile = self.create_user()
        self.auction, _ = Auction.objects.get_or_create(name='New Auction',
                                                     description='Description big',
                                                     date_start=update_date_timzone('2020-10-11', '%Y-%m-%d'),
                                                     date_end=update_date_timzone('2020-11-11', '%Y-%m-%d'),
                                                     rate_start='1000',
                                                     author=self.user)
        self.path_pk = reverse('auction_finish_pk', args=[self.auction.pk])

    def test_put(self):
        data = {
            "name": 'Auction2',
            "description": 'Description new',
            "date_start": '2020-10-12 10:00:00',
            "date_end": '2020-10-13 10:00:00',
            "rate_start": '2500'
        }
        response = self.client.put(self.path_pk, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        response = self.client.delete(self.path_pk)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)