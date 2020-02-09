import urllib.parse

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from .models import Greeting


def query_dict_from_request(request, debug = False):
  query = urllib.parse.urlparse(request).query
  request_query_dict = (dict(urllib.parse.parse_qsl(query)))

  if debug:
    for key in request_query_dict:
      print(key + ': ' + request_query_dict[key])

  return request_query_dict

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def api(request):
    return HttpResponse("{}")

def auth(request):
    request_query_dict = query_dict_from_request(str(request))

    # TODO: Ask for password/login or something before giving auth_code!

    redirect_uri = request_query_dict['redirect_uri']
    auth_code = 'AUTH_CODE_HERE'
    state = request_query_dict['state']

    params = urllib.parse.urlencode(
      {
        'code': auth_code,
        'state': state
      }
    )

    result = redirect_uri + '?' + params

    return redirect(result)


def token(request):
    return HttpResponse("{}")

