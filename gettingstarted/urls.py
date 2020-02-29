from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

import hello.views

admin.autodiscover()

urlpatterns = [
    path('', RedirectView.as_view(url='admin/')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("admin/", admin.site.urls),
    path("api/", hello.views.api),
    path("auth/", hello.views.auth),
    path("token/", hello.views.token),
]
