from django.contrib import admin
from django.urls import include, path

import hello.views

admin.autodiscover()

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path("", hello.views.index, name="index"),
    path("api/", hello.views.api),
    path("auth/", hello.views.auth),
    path("token/", hello.views.token),
    path("admin/", admin.site.urls),
]
