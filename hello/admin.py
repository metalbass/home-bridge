from django.contrib import admin

from .models import Greeting, AuthToken, AccessToken, RefreshToken, SecretData

admin.site.register(Greeting)
admin.site.register(SecretData)
admin.site.register(AuthToken)
admin.site.register(AccessToken)
admin.site.register(RefreshToken)
