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

    def grant_access_token(self, parameters: dict):
        if not self.is_client_secret_accepted(parameters['client_id'], parameters['client_secret']):
            raise UnauthorizedError

        result_dict = {
            'token_type': 'bearer',
            'expires_in': int(AccessToken.ExpirationTime.total_seconds()),
        }

        grant_type = parameters['grant_type']

        if grant_type == 'authorization_code':
            auth_token = self.auth_token_manager.get(token=parameters['code'])

            if auth_token is None:
                raise UnauthorizedError

            if timezone.now() > auth_token.expiration:
                raise TokenExpiredError

            access_token = self.access_token_manager.create()
            refresh_token = self.refresh_token_manager.create()

            result_dict['access_token'] = access_token.token
            result_dict['refresh_token'] = refresh_token.token

        elif grant_type == 'refresh_token':
            refresh_token = RefreshToken.objects.filter(token=parameters['refresh_token'])

            if not refresh_token.exists():
                raise UnauthorizedError

            access_token = self.access_token_manager.create()

            result_dict['access_token'] = access_token.token

        return result_dict
