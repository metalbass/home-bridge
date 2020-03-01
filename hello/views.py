import json
import urllib.parse

from django import shortcuts
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .models.oauth import SecretData
from .oauth import OAuth, UnauthorizedError, TokenExpiredError
from .smarthome import SmartHome

secret = SecretData.load()

oauth = OAuth(accepted_redirect_locations={'oauth-redirect.googleusercontent.com'},
              accepted_clients={secret.client_id: secret.client_secret})

smartHome = SmartHome()


def get_request_parameters(request: HttpRequest):
    query = urllib.parse.urlparse(str(request)).query
    request_query_dict = dict(urllib.parse.parse_qsl(query))

    return request_query_dict


@csrf_exempt
def api(request: HttpRequest) -> HttpResponse:
    request_dict = json.loads(request.body)
    response_dict = smartHome.process_fulfillment(request_dict, request.headers['Authorization'])

    print('REQUEST:%s\nRESPONSE:%s' % (request_dict, response_dict))

    return HttpResponse(json.dumps(response_dict, indent=2), content_type='application/json')


@login_required
def auth(request: HttpRequest):
    if request.method != 'GET':
        return HttpResponseNotAllowed('Not Allowed!')

    try:
        redirect = oauth.grant_auth_token(get_request_parameters(request))
    except UnauthorizedError:
        return HttpResponseForbidden('Forbidden!')

    return shortcuts.render(request, 'auth_link.html', context={'next': redirect})


@csrf_exempt
def token(request: HttpRequest):
    invalid_grant_response = HttpResponseBadRequest('{"error": "invalid_grant"}')

    if request.method != 'POST':
        return invalid_grant_response

    try:
        result_dict = oauth.grant_access_token(request.POST)
    except (UnauthorizedError, TokenExpiredError):
        return invalid_grant_response

    return HttpResponse(json.dumps(result_dict), content_type='application/json')
