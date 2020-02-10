import secrets

from django.utils import timezone
from datetime import datetime, timedelta
from django.db import models


def generate_hex_token(size: int = 16) -> str:
    return secrets.token_hex(size)


def generate_expiration_date(expiration_time: timedelta = timedelta(hours=24)) -> datetime:
    return timezone.now() + expiration_time


class SecretData(models.Model):
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    client_id = models.CharField(max_length=32)
    client_secret = models.CharField(max_length=32)

class AuthToken(models.Model):
    ExpirationTime = timedelta(minutes=10)

    token = models.CharField(primary_key=True, max_length=32, default=generate_hex_token)
    expiration = models.DateTimeField(default=generate_expiration_date)


class AccessToken(models.Model):
    ExpirationTime = timedelta(hours=24)

    token = models.CharField(primary_key=True, max_length=32, default=generate_hex_token)
    expiration = models.DateTimeField(default=generate_expiration_date)


class RefreshToken(models.Model):
    token = models.CharField(primary_key=True, max_length=32, default=generate_hex_token)
