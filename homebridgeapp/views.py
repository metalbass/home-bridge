import json
import urllib.parse

import django.apps.registry
import django.shortcuts
import django.http

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotAllowed

from . import oauth

app = django.apps.registry.apps.get_app_config('homebridgeapp')


def get_request_parameters(request: HttpRequest):
    query = urllib.parse.urlparse(str(request)).query
    request_query_dict = dict(urllib.parse.parse_qsl(query))

    return request_query_dict


@csrf_exempt
def api(request: HttpRequest) -> HttpResponse:
    request_dict = json.loads(request.body)
    response_dict = app.smart_home.process_fulfillment(request_dict, request.headers['Authorization'])

    print('REQUEST:%s\nRESPONSE:%s' % (request_dict, response_dict))

    return HttpResponse(json.dumps(response_dict, indent=2), content_type='application/json')


@login_required
def auth(request: HttpRequest):
    if request.method != 'GET':
        return HttpResponseNotAllowed('Not Allowed!')

    parameters = get_request_parameters(request)

    try:
        redirect = app.oauth.grant_auth_token(parameters['redirect_uri'], parameters['client_id'],
                                              parameters['state'])
    except oauth.UnauthorizedError:
        return HttpResponseForbidden('Forbidden!')

    return django.shortcuts.render(request, 'auth_link.html', context={'next': redirect})


@csrf_exempt
def token(request: HttpRequest):
    invalid_grant_response = HttpResponseBadRequest('{"error": "invalid_grant"}')

    if request.method != 'POST':
        return invalid_grant_response

    try:
        if request.POST['grant_type'] == 'authorization_code':
            result = app.oauth.grant_access_token(request.POST['client_id'], request.POST['client_secret'],
                                                  request.POST['auth_token'])
        else:
            result = app.oauth.refresh_access_token(request.POST['client_id'], request.POST['client_secret'],
                                                    request.POST['refresh_token'])

    except (oauth.UnauthorizedError, oauth.TokenExpiredError):
        return invalid_grant_response

    return HttpResponse(json.dumps(result), content_type='application/json')
