from django.test import TestCase

from ..models.devices import Device, Blind
from..oauth import OAuth


class OAuthTests(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.known_client = 'known_client'
        self.valid_secret = 'valid_secret'

        self.oauth = OAuth(accepted_clients={self.known_client: self.valid_secret})

    def test_known_client_id_is_accepted(self):
        self.assertTrue(self.oauth.is_client_accepted(self.known_client))

    def test_unknown_client_id_is_not_accepted(self):
        self.assertFalse(self.oauth.is_client_accepted('unknown_client'))

    def test_known_client_valid_secret_is_accepted(self):
        self.assertTrue(self.oauth.is_client_secret_accepted(self.known_client, self.valid_secret))

    def test_known_client_invalid_secret_is_not_accepted(self):
        self.assertFalse(self.oauth.is_client_secret_accepted(self.known_client, 'invalid_secret'))

    def test_unknown_client_valid_secret_is_not_accepted(self):
        self.assertFalse(self.oauth.is_client_secret_accepted('unknown_client', self.valid_secret))

    def test_unknown_client_invalid_secret_is_not_accepted(self):
        self.assertFalse(self.oauth.is_client_secret_accepted('unknown_client', 'invalid_secret'))
