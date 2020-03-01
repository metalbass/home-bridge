from unittest.mock import Mock

from django.test import TestCase

from ..models.oauth import AuthToken
from ..oauth import OAuth, UnauthorizedError


class OAuthTests(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.known_client = 'known_client'
        self.known_redirect = 'http://www.known.net/login'
        self.valid_secret = 'valid_secret'

        self.oauth = OAuth(accepted_redirect_locations=['www.known.net'],
                           accepted_clients={self.known_client: self.valid_secret})

    def test_known_location_is_accepted(self):
        self.assertTrue(self.oauth.is_redirect_accepted(self.known_redirect))

    def test_unknown_location_is_not_accepted(self):
        self.assertFalse(self.oauth.is_redirect_accepted('http://www.unknown.net/login'))

    def test_empty_redirect_is_not_accepted(self):
        self.assertFalse(self.oauth.is_redirect_accepted(''))

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

    def test_grant_auth_token_returns_new_token(self):
        self.oauth.auth_token_manager = Mock()
        self.oauth.auth_token_manager.create = Mock(return_value=AuthToken(token='token1234'))

        self.assertURLEqual(self.known_redirect + '?code=token1234&state=state1234',
                            self.oauth.grant_auth_token(self.known_redirect, self.known_client, 'state1234'))

    def test_grant_auth_token_raises_unauthorized_location(self):
        with self.assertRaises(UnauthorizedError):
            self.oauth.grant_auth_token('google.com', self.known_client, 'state1234')

    def test_grant_auth_token_raises_unauthorized_client(self):
        with self.assertRaises(UnauthorizedError):
            self.oauth.grant_auth_token(self.known_redirect, 'unknown_client', 'state1234')
