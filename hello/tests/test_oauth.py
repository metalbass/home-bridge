from unittest.mock import Mock
from contextlib import suppress

from django.test import TestCase
from django.utils import timezone

from ..models.oauth import AuthToken, AccessToken, RefreshToken
from ..oauth import OAuth, UnauthorizedError, TokenExpiredError


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
        self.oauth.auth_token_manager.create = Mock(return_value=AuthToken(token='auth1234'))

        self.assertURLEqual(self.known_redirect + '?code=auth1234&state=state1234',
                            self.oauth.grant_auth_token(self.known_redirect, self.known_client, 'state1234'))

    def test_grant_auth_token_raises_unauthorized_location(self):
        with self.assertRaises(UnauthorizedError):
            self.oauth.grant_auth_token('google.com', self.known_client, 'state1234')

    def test_grant_auth_token_raises_unauthorized_client(self):
        with self.assertRaises(UnauthorizedError):
            self.oauth.grant_auth_token(self.known_redirect, 'unknown_client', 'state1234')

    def test_grant_access_token_raises_unauthorized_client_id(self):
        with self.assertRaises(UnauthorizedError):
            self.oauth.grant_access_token('unknown_client', self.valid_secret, 'auth1234')

    def test_grant_access_token_raises_unauthorized_client_secret(self):
        with self.assertRaises(UnauthorizedError):
            self.oauth.grant_access_token(self.known_client, 'invalid_secret', 'auth1234')

    def test_grant_access_token_raises_unauthorized_auth_token(self):
        with self.assertRaises(UnauthorizedError):
            self.oauth.grant_access_token(self.known_client, self.valid_secret, 'auth1234')

    def test_grant_access_token_raises_token_expired(self):
        AuthToken.objects.create(token='auth1234', expiration=timezone.now())

        with self.assertRaises(TokenExpiredError):
            self.oauth.grant_access_token(self.known_client, self.valid_secret, 'auth1234')

    def test_grant_access_token_deletes_expired_token(self):
        AuthToken.objects.create(token='auth1234', expiration=timezone.now())

        with suppress(TokenExpiredError):
            self.oauth.grant_access_token(self.known_client, self.valid_secret, 'auth1234')

        self.assertEquals(0, AuthToken.objects.count())

    def test_grant_access_token_deletes_auth_token(self):
        AuthToken.objects.create(token='auth1234')

        self.oauth.grant_access_token(self.known_client, self.valid_secret, 'auth1234')

        self.assertEquals(0, AuthToken.objects.count())

    def test_grant_access_token_returns_dict(self):
        AuthToken.objects.create(token='auth1234')

        self.oauth.access_token_manager = Mock()
        self.oauth.access_token_manager.create = Mock(return_value=AccessToken(token='access1234'))

        self.oauth.refresh_token_manager = Mock()
        self.oauth.refresh_token_manager.create = Mock(return_value=RefreshToken(token='refresh1234'))

        expected_result = {
            'token_type': 'bearer',
            'expires_in': int(AccessToken.ExpirationTime.total_seconds()),
            'access_token': 'access1234',
            'refresh_token': 'refresh1234'
        }

        self.assertEquals(expected_result,
                          self.oauth.grant_access_token(self.known_client, self.valid_secret, 'auth1234'))

    def test_refresh_access_token_raises_unauthorized_client_id(self):
        with self.assertRaises(UnauthorizedError):
            self.oauth.refresh_access_token('unknown_client', self.valid_secret, 'refresh1234')

    def test_refresh_access_token_raises_unauthorized_client_secret(self):
        with self.assertRaises(UnauthorizedError):
            self.oauth.refresh_access_token(self.known_client, 'invalid_secret', 'refresh1234')

    def test_refresh_access_token_raises_unauthorized_refresh_token(self):
        with self.assertRaises(UnauthorizedError):
            self.oauth.refresh_access_token(self.known_client, self.valid_secret, 'refresh1234')

    def test_refresh_access_token_returns_dict(self):
        RefreshToken.objects.create(token='refresh1234')

        self.oauth.access_token_manager = Mock()
        self.oauth.access_token_manager.create = Mock(return_value=AccessToken(token='access1234'))

        expected_result = {
            'token_type': 'bearer',
            'expires_in': int(AccessToken.ExpirationTime.total_seconds()),
            'access_token': 'access1234',
        }

        self.assertEquals(expected_result,
                          self.oauth.refresh_access_token(self.known_client, self.valid_secret, 'refresh1234'))

