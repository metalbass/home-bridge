from unittest.mock import Mock

import django.http
import django.test
from django.contrib.auth.models import User

from .. import oauth


class LoggedOutViewTests(django.test.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.app = django.apps.registry.apps.get_app_config('homebridgeapp')

    def test_auth_without_login_redirects(self):
        response = self.client.get('/auth/')

        self.assertRedirects(response, '/accounts/login/?next=/auth/')

    def test_token_get_is_bad_request(self):
        response = self.client.get('/token/')

        self.assertEqual(response.status_code, django.http.HttpResponseBadRequest.status_code)

    def test_auth_token_unauthorized_is_bad_request(self):
        self.app.oauth = Mock()
        self.app.oauth.grant_access_token = Mock(side_effect=oauth.UnauthorizedError)

        response = self.client.post('/token/', {
            'grant_type': 'authorization_code',
            'client_id': 'client1234',
            'client_secret': 'secret1234',
            'auth_token': 'auth1234'
        })

        self.assertEqual(response.status_code, django.http.HttpResponseBadRequest.status_code)

    def test_auth_token_expired_is_bad_request(self):
        self.app.oauth = Mock()
        self.app.oauth.grant_access_token = Mock(side_effect=oauth.TokenExpiredError)

        response = self.client.post('/token/', {
            'grant_type': 'authorization_code',
            'client_id': 'client1234',
            'client_secret': 'secret1234',
            'auth_token': 'auth1234'
        })

        self.assertEqual(response.status_code, django.http.HttpResponseBadRequest.status_code)

    def test_refresh_token_unauthorized_is_bad_request(self):
        self.app.oauth = Mock()
        self.app.oauth.refresh_access_token = Mock(side_effect=oauth.UnauthorizedError)

        response = self.client.post('/token/', {
            'grant_type': 'refresh_token',
            'client_id': 'client1234',
            'client_secret': 'secret1234',
            'refresh_token': 'auth1234'
        })

        self.assertEqual(response.status_code, django.http.HttpResponseBadRequest.status_code)

    def test_token_returns_json(self):
        self.app.oauth = Mock()
        self.app.oauth.grant_access_token = Mock(return_value={})

        response = self.client.post('/token/', {
            'grant_type': 'authorization_code',
            'client_id': 'client1234',
            'client_secret': 'secret1234',
            'auth_token': 'auth1234'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, "{}")


class LoggedInViewTests(django.test.TestCase):
    def setUp(self):
        self.maxDiff = None

        User.objects.create_user('john', 'address@email.com', 'pass1234')
        self.client.login(username='john', password='pass1234')

        self.app = django.apps.registry.apps.get_app_config('homebridgeapp')

    def test_auth_post_is_not_allowed(self):
        response = self.client.post('/auth/')
        self.assertEqual(response.status_code, django.http.HttpResponseNotAllowed.status_code)

    def test_auth_is_forbidden_if_oauth_not_authorized(self):
        self.app.oauth = Mock()
        self.app.oauth.grant_auth_token = Mock(side_effect=oauth.UnauthorizedError)

        response = self.client.get('/auth/', {'redirect_uri': 'asd', 'client_id': 'asd', 'state': 'asd'})

        self.assertEqual(response.status_code, django.http.HttpResponseForbidden.status_code)

    def test_auth_renders_auth_if_oauth_is_authorized(self):
        self.app.oauth = Mock()
        self.app.oauth.grant_auth_token = Mock(return_value='www.google.com')

        response = self.client.get('/auth/', {'redirect_uri': 'asd', 'client_id': 'asd', 'state': 'asd'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_link.html')
        self.assertEqual(response.context['next'], 'www.google.com')
