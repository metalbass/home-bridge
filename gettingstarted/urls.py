from django.contrib import admin
from django.urls import path

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("api/", hello.views.api),
    path("auth/", hello.views.auth),
    path("token/", hello.views.token),
    path("admin/", admin.site.urls),
]
