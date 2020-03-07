from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

import homebridgeapp.views

admin.autodiscover()

urlpatterns = [
    path('', RedirectView.as_view(url='admin/')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("admin/", admin.site.urls),
    path("api/", homebridgeapp.views.api),
    path("auth/", homebridgeapp.views.auth),
    path("token/", homebridgeapp.views.token),
]
