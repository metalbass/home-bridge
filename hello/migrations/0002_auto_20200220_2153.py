# Generated by Django 3.0.3 on 2020-02-20 20:53

import collectionfield.models.fields
from django.db import migrations, models
import hello.models.devices


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='attributes',
            field=models.CharField(default='{}', max_length=1024),
        ),
        migrations.AlterField(
            model_name='device',
            name='traits',
            field=collectionfield.models.fields.CollectionField(choices=[('action.devices.traits.OnOff', 'On Off'), ('action.devices.traits.OpenClose', 'Open Close')], collection_type=set, item_type=hello.models.devices.Device.Trait),
        ),
        migrations.AlterField(
            model_name='device',
            name='type',
            field=models.CharField(choices=[('action.devices.types.LIGHT', 'Light'), ('action.devices.types.BLINDS', 'Blinds')], max_length=64),
        ),
    ]
