import json
import urllib.parse

from django import shortcuts
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import oauth
from .smarthome import SmartHome

smartHome = SmartHome()


def get_request_parameters(request: HttpRequest):
    query = urllib.parse.urlparse(str(request)).query
    request_query_dict = dict(urllib.parse.parse_qsl(query))

    return request_query_dict


@csrf_exempt
def api(request: HttpRequest):
    response_dict = smartHome.process_fulfillment(json.loads(request.body))

    return HttpResponse(json.dumps(response_dict, indent=2), content_type='application/json')


@login_required
def auth(request: HttpRequest):
    if request.method != 'GET':
        return HttpResponseNotAllowed('Not Allowed!')

    request_parameters = get_request_parameters(request)

    client_id = request_parameters['client_id']
    redirect_uri = request_parameters['redirect_uri']

    if (urllib.parse.urlparse(redirect_uri).netloc != 'oauth-redirect.googleusercontent.com'
            or client_id != oauth.SecretData.load().client_id):
        return HttpResponseForbidden('Forbidden!')

    state = request_parameters['state']

    auth_token = oauth.AuthToken()
    auth_token.save()

    response_parameters = urllib.parse.urlencode({
        'code': auth_token.token,
        'state': state
    })

    redirect_with_parameters = redirect_uri + '?' + response_parameters

    return shortcuts.render(request, 'auth_link.html', context={'next': redirect_with_parameters})


@csrf_exempt
def token(request: HttpRequest):
    invalid_grant_response = HttpResponseBadRequest('{"error": "invalid_grant"}')

    if request.method != 'POST':
        return invalid_grant_response

    client_id = request.POST['client_id']
    client_secret = request.POST['client_secret']

    secret = oauth.SecretData.load()

    if (secret.client_id != client_id
            or secret.client_secret != client_secret):
        print('Failed to validate secret pair!\n%s:%s' % (client_id, client_secret))
        return invalid_grant_response

    result_dict = {
        'token_type': 'bearer',
        'expires_in': int(oauth.AccessToken.ExpirationTime.total_seconds()),
    }

    grant_type = request.POST['grant_type']

    if grant_type == 'authorization_code':
        auth_token = oauth.AuthToken.objects.get(token=request.POST['code'])

        if auth_token is None:
            print('no auth_token found')
            return invalid_grant_response

        if timezone.now() > auth_token.expiration:  # token expired
            # TODO: delete token?
            print('token expired')
            return invalid_grant_response

        access_token = oauth.AccessToken()
        access_token.save()
        refresh_token = oauth.RefreshToken()
        refresh_token.save()

        result_dict['access_token'] = access_token.token
        result_dict['refresh_token'] = refresh_token.token

    elif grant_type == 'refresh_token':
        if not oauth.RefreshToken.objects.filter(token=request.POST['refresh_token']).exists():
            print('no refresh_token found')
            return invalid_grant_response

        access_token = oauth.AccessToken()
        access_token.save()

        result_dict['access_token'] = access_token.token

    return HttpResponse(json.dumps(result_dict), content_type='application/json')
