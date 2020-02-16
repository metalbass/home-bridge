from django.contrib import admin
from django.urls import path
import hello.views

admin.autodiscover()

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("api/", hello.views.api),
    path("auth/", hello.views.auth),
    path("token/", hello.views.token),
    path("admin/", admin.site.urls),
]
