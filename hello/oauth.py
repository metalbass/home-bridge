import urllib.parse

from django.utils import timezone

from .models.oauth import AuthToken, AccessToken, RefreshToken


class UnauthorizedError(Exception):
    pass


class TokenExpiredError(Exception):
    pass


class OAuth:
    def __init__(self, accepted_redirect_locations=None, accepted_clients=None):
        self.accepted_redirect_locations = set(accepted_redirect_locations or set())
        self.accepted_clients = dict(accepted_clients or dict())

    def is_client_accepted(self, client_id) -> bool:
        return client_id in self.accepted_clients

    def is_client_secret_accepted(self, client_id, client_secret) -> bool:
        found_secret = self.accepted_clients.get(client_id)
        return found_secret and found_secret == client_secret

    def grant_auth_token(self, parameters: dict) -> str:
        redirect_uri = parameters['redirect_uri']

        if (urllib.parse.urlparse(redirect_uri).netloc not in self.accepted_redirect_locations or
                not self.is_client_accepted(parameters['client_id'])):
            raise UnauthorizedError

        auth_token = AuthToken.objects.create()

        response_parameters = urllib.parse.urlencode({
            'code': auth_token.token,
            'state': parameters['state']
        })

        return redirect_uri + '?' + response_parameters

    def grant_access_token(self, parameters: dict):
        if not self.is_client_secret_accepted(parameters['client_id'], parameters['client_secret']):
            raise UnauthorizedError

        result_dict = {
            'token_type': 'bearer',
            'expires_in': int(AccessToken.ExpirationTime.total_seconds()),
        }

        grant_type = parameters['grant_type']

        if grant_type == 'authorization_code':
            auth_token = AuthToken.objects.get(token=parameters['code'])

            if auth_token is None:
                raise UnauthorizedError

            if timezone.now() > auth_token.expiration:
                raise TokenExpiredError

            access_token = AccessToken.objects.create()
            refresh_token = RefreshToken.objects.create()

            result_dict['access_token'] = access_token.token
            result_dict['refresh_token'] = refresh_token.token

        elif grant_type == 'refresh_token':
            refresh_token = RefreshToken.objects.filter(token=parameters['refresh_token'])

            if not refresh_token.exists():
                raise UnauthorizedError

            access_token = AccessToken.objects.create()

            result_dict['access_token'] = access_token.token

        return result_dict
