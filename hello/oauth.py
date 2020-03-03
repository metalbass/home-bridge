import urllib.parse

from django.utils import timezone

from .models.oauth import AuthToken, AccessToken, RefreshToken


class UnauthorizedError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class TokenExpiredError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class OAuth:
    def __init__(self, accepted_redirect_locations=None, accepted_clients=None,
                 auth_token_manager=None, access_token_manager=None, refresh_token_manager=None):
        self.accepted_redirect_locations = set(accepted_redirect_locations or set())
        self.accepted_clients = dict(accepted_clients or dict())

        self.auth_token_manager = auth_token_manager or AuthToken.objects
        self.access_token_manager = access_token_manager or AccessToken.objects
        self.refresh_token_manager = refresh_token_manager or RefreshToken.objects

    def is_redirect_accepted(self, redirect):
        return urllib.parse.urlparse(redirect).netloc in self.accepted_redirect_locations

    def is_client_accepted(self, client_id) -> bool:
        return client_id in self.accepted_clients

    def is_client_secret_accepted(self, client_id, client_secret) -> bool:
        found_secret = self.accepted_clients.get(client_id)
        return found_secret and found_secret == client_secret

    def grant_auth_token(self, redirect, client_id, state) -> str:
        # Should tokens be related to users?

        if not self.is_redirect_accepted(redirect):
            raise UnauthorizedError('redirect location not allowed ' + redirect)

        if not self.is_client_accepted(client_id):
            raise UnauthorizedError('client not allowed ' + client_id)

        auth_token = self.auth_token_manager.create()

        response_parameters = urllib.parse.urlencode({
            'code': auth_token.token,
            'state': state
        })

        return redirect + '?' + response_parameters

    def grant_access_token(self, client_id, client_secret, auth_token):
        if not self.is_client_secret_accepted(client_id, client_secret):
            raise UnauthorizedError('client not allowed %s %s' % (client_id, client_secret))

        db_auth_token = self.auth_token_manager.filter(token=auth_token)

        if not db_auth_token.exists():
            raise UnauthorizedError('auth token does not exist ' + auth_token)

        did_token_expire = timezone.now() >= db_auth_token[0].expiration
        db_auth_token.delete()

        if did_token_expire:
            raise TokenExpiredError

        return {
            'token_type': 'bearer',
            'expires_in': int(AccessToken.ExpirationTime.total_seconds()),
            'access_token': self.access_token_manager.create().token,
            'refresh_token': self.refresh_token_manager.create().token
        }

    def refresh_access_token(self, client_id, client_secret, refresh_token):
        if not self.is_client_secret_accepted(client_id, client_secret):
            raise UnauthorizedError('client not allowed %s %s' % (client_id, client_secret))

        db_token = self.refresh_token_manager.filter(token=refresh_token)

        if not db_token.exists():
            raise UnauthorizedError('refresh token does not exist ' + refresh_token)

        return {
            'token_type': 'bearer',
            'expires_in': int(AccessToken.ExpirationTime.total_seconds()),
            'access_token': self.access_token_manager.create().token
        }
