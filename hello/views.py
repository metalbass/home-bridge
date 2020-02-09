import urllib.parse

from django import http, shortcuts
from .models import Greeting


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


def api(request):
    return http.HttpResponse("{}")


def auth(request):
    # TODO: ensure it's a GET request
    # TODO: Ask for password/login or something before giving auth_code!

    request_parameters = get_request_parameters(request)

    redirect_uri = request_parameters['redirect_uri']
    auth_code = 'AUTH_CODE_HERE'
    state = request_parameters['state']

    response_parameters = urllib.parse.urlencode(
        {
            'code': auth_code,
            'state': state
        }
    )

    redirect_with_parameters = redirect_uri + '?' + response_parameters

    # return http.HttpResponseRedirect(redirect_with_parameters)

    return http.HttpResponse('<a href="%s">Link</a>' % redirect_with_parameters)


def token(request):
    # TODO: make sure it's a POST request

    json_res = {
        'token_type': 'bearer',
        'access_token': '123access',
        'expires_in': 24 * 60 * 60,  # 24h in seconds
    }

    request_parameters = get_request_parameters(request)
    grant_type = request_parameters['grant_type']

    if grant_type == 'authorization_code':
        json_res['refresh_token'] = '123refresh'

    return http.HttpResponse(str(json_res), content_type='application/json')
