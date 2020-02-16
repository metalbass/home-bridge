from django.contrib import admin

from .models import oauth

admin.site.register(oauth.SecretData)
admin.site.register(oauth.AuthToken)
admin.site.register(oauth.AccessToken)
admin.site.register(oauth.RefreshToken)
