import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework.authtoken.models import Token

from .models import Asset

User = get_user_model()


class AssetTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='samuel@gmail.com', username='samuel', password='admin123')
        self.token = Token.objects.create(user=self.user).key
        self.asset1 = Asset.objects.create(name="asset1",
                                           mode=Asset.ModeChoices.fixed_income,
                                           created_by=self.user)
        self.asset2 = Asset.objects.create(name="asset2",
                                           mode=Asset.ModeChoices.variable_income,
                                           created_by=self.user)
        self.asset3 = Asset.objects.create(name="asset3",
                                           mode=Asset.ModeChoices.crypto,
                                           created_by=self.user)

    def test_listing_asset_unauthorized(self):
        response = self.client.get(reverse('api:asset:listing'))
        self.assertEqual(response.status_code, 401)

    def test_listing_asset_authorized(self):
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
        response = self.client.get(reverse('api:asset:listing'), **header)
        self.assertEqual(response.status_code, 200)

    def test_listing_asset(self):
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
        response = self.client.get("{}?mode_filter={}".format(reverse('api:asset:listing'),
                                                              Asset.ModeChoices.fixed_income), **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_asset(self):
        header = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(self.token),
            'content_type': 'application/json'
        }
        asset_data = {
            "name": "asset4",
            "mode": Asset.ModeChoices.fixed_income,
        }
        response = self.client.post(reverse('api:asset:created'), json.dumps(asset_data), **header)
        self.assertEqual(response.status_code, 201)


class TransactionTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='samuel@gmail.com', username='samuel', password='admin123')
        self.token = Token.objects.create(user=self.user).key
        self.asset = Asset.objects.create(name="asset1",
                                          mode=Asset.ModeChoices.fixed_income,
                                          created_by=self.user)

    def test_create_transaction_unauthorized(self):
        response = self.client.get(reverse('api:transaction:created'))
        self.assertEqual(response.status_code, 401)

    def test_create_transaction(self):
        header = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(self.token),
            'content_type': 'application/json'
        }
        asset_transaction = {
            "asset": str(self.asset.id),
            "amount": 2,
            "unit_price": 250,
            "ip_address": "127.0.0.1",
            "request_date": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "is_redemption": True
        }
        response = self.client.post(reverse('api:transaction:created'), json.dumps(asset_transaction), **header)
        self.assertEqual(response.status_code, 201)


class PortfolioTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='samuel@gmail.com', username='samuel', password='admin123')
        self.token = Token.objects.create(user=self.user).key

    def test_portfolio_unauthorized(self):
        response = self.client.get(reverse('api:portfolio'))
        self.assertEqual(response.status_code, 401)

    def test_portfolio_authorized(self):
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
        response = self.client.get(reverse('api:portfolio'), **header)
        self.assertEqual(response.status_code, 200)
