from django.apps import AppConfig
import django.db.utils


class HomeBridgeAppConfig(AppConfig):
    name = 'homebridgeapp'
    verbose_name = 'Home Bridge App'

    # noinspection PyAttributeOutsideInit
    def ready(self):
        from .smarthome import SmartHome
        from .oauth import OAuth

        self.smart_home = SmartHome()

        self.oauth = OAuth(accepted_redirect_locations={'oauth-redirect.googleusercontent.com'},
                           accepted_clients=HomeBridgeAppConfig.load_client_and_secret())

    @staticmethod
    def load_client_and_secret():
        from .models.oauth import SecretData

        try:
            secret = SecretData.load()
            return {secret.client_id: secret.client_secret}

        except django.db.utils.OperationalError as e:
            print('Initializing with dummy client_id & client_secret, as ' + str(e))
            return {'': ''}


