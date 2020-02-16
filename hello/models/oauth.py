import secrets

from django.utils import timezone
from datetime import datetime, timedelta

from django.db.models import Model, CharField, DateTimeField


def generate_hex_token(size: int = 16) -> str:
    return secrets.token_hex(size)


def generate_expiration_date(expiration_time: timedelta = timedelta(hours=24)) -> datetime:
    return timezone.now() + expiration_time


class SecretData(Model):
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    client_id = CharField(max_length=32)
    client_secret = CharField(max_length=32)


class AuthToken(Model):
    ExpirationTime = timedelta(minutes=10)

    token = CharField(primary_key=True, max_length=32, default=generate_hex_token)
    expiration = DateTimeField(default=generate_expiration_date)


class AccessToken(Model):
    ExpirationTime = timedelta(hours=24)

    token = CharField(primary_key=True, max_length=32, default=generate_hex_token)
    expiration = DateTimeField(default=generate_expiration_date)


class RefreshToken(Model):
    token = CharField(primary_key=True, max_length=32, default=generate_hex_token)
