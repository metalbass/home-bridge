import os
from django.apps import AppConfig



class HomeBridgeAppConfig(AppConfig):
    name = 'homebridgeapp'
    verbose_name = 'Home Bridge App'

    # noinspection PyAttributeOutsideInit
    def ready(self):
        from .smarthome import SmartHome
        from .models.oauth import SecretData
        from .oauth import OAuth

        if os.environ.get('RUN_MAIN'):
            self.smart_home = SmartHome()

            secret = SecretData.load()

            self.oauth = OAuth(accepted_redirect_locations={'oauth-redirect.googleusercontent.com'},
                               accepted_clients={secret.client_id: secret.client_secret})
