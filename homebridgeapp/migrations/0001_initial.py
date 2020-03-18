# Generated by Django 3.0.4 on 2020-03-18 09:13

from django.db import migrations, models
import homebridgeapp.models.oauth


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('token', models.CharField(default=homebridgeapp.models.oauth.generate_hex_token, max_length=32, primary_key=True, serialize=False)),
                ('expiration', models.DateTimeField(default=homebridgeapp.models.oauth.generate_expiration_date)),
            ],
        ),
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('token', models.CharField(default=homebridgeapp.models.oauth.generate_hex_token, max_length=32, primary_key=True, serialize=False)),
                ('expiration', models.DateTimeField(default=homebridgeapp.models.oauth.generate_expiration_date)),
            ],
        ),
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('will_report_state', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Blind',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('will_report_state', models.BooleanField(default=False)),
                ('open_percent', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RefreshToken',
            fields=[
                ('token', models.CharField(default=homebridgeapp.models.oauth.generate_hex_token, max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SecretData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=32)),
                ('client_secret', models.CharField(max_length=32)),
            ],
        ),
    ]