import json
import urllib.parse

from django import http, shortcuts
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Greeting, AuthToken, AccessToken, RefreshToken, SecretData


def get_request_parameters(request: http.HttpRequest, debug: bool = False):
    query = urllib.parse.urlparse(str(request)).query
    request_query_dict = dict(urllib.parse.parse_qsl(query))

    if debug:
        for key in request_query_dict:
            print(key + ': ' + request_query_dict[key])

    return request_query_dict


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return shortcuts.render(request, 'index.html')


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return shortcuts.render(request, 'db.html', {'greetings': greetings})


@csrf_exempt
def api(request: http.HttpRequest):
    print(str(request))
    print(str(get_request_parameters(request)))
    print(str(request.POST))

    return http.HttpResponse("{}")


def auth(request: http.HttpRequest):
    if request.method != 'GET':
        return http.HttpResponseNotAllowed('Not Allowed!')

    request_parameters = get_request_parameters(request)

    client_id = request_parameters['client_id']
    redirect_uri = request_parameters['redirect_uri']

    if (urllib.parse.urlparse(redirect_uri).netloc != 'oauth-redirect.googleusercontent.com'
            or client_id != SecretData.load().client_id):
        return http.HttpResponseForbidden('Forbidden!')

    # TODO: Ask for password/login or something before giving auth_code!

    state = request_parameters['state']

    auth_token = AuthToken()
    auth_token.save()

    response_parameters = urllib.parse.urlencode(
        {
            'code': auth_token.token,
            'state': state
        }
    )

    redirect_with_parameters = redirect_uri + '?' + response_parameters

    # return http.HttpResponseRedirect(redirect_with_parameters)

    return http.HttpResponse('<a href="%s">Link</a>' % redirect_with_parameters)


@csrf_exempt
def token(request: http.HttpRequest):
    invalid_grant_response = http.HttpResponseBadRequest('{"error": "invalid_grant"}')

    if request.method != 'POST':
        return invalid_grant_response

    client_id = request.POST['client_id']
    client_secret = request.POST['client_secret']

    secret = SecretData.load()

    if (secret.client_id != client_id
            or secret.client_secret != client_secret):
        print('Failed to validate secret pair!\n%s:%s' % (client_id, client_secret))
        return invalid_grant_response

    result_dict = {
        'token_type': 'bearer',
        'expires_in': int(AccessToken.ExpirationTime.total_seconds()),
    }

    grant_type = request.POST['grant_type']

    if grant_type == 'authorization_code':
        auth_token = AuthToken.objects.get(token=request.POST['code'])

        if auth_token is None:
            print('no auth_token found')
            return invalid_grant_response

        if timezone.now() > auth_token.expiration:  # token expired
            # TODO: delete token?
            print('token expired')
            return invalid_grant_response

        access_token = AccessToken()
        access_token.save()
        refresh_token = RefreshToken()
        refresh_token.save()

        result_dict['access_token'] = access_token.token
        result_dict['refresh_token'] = refresh_token.token

    elif grant_type == 'refresh_token':
        refresh_token = RefreshToken.objects.get(token=request.POST['refresh_token'])

        if refresh_token is None:
            print('no refresh_token found')
            return invalid_grant_response

        access_token = AccessToken()
        access_token.save()

        result_dict['access_token'] = access_token.token

    return http.HttpResponse(json.dumps(result_dict), content_type='application/json')
