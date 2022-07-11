# Generated by Django 4.0.4 on 2022-07-10 23:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_dicomserver_is_running'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicomserver',
            name='ae_title',
            field=models.CharField(default='ANY-SCP', help_text='An AE Title for the DICOM server. The default is ANY-SCP', max_length=64, verbose_name='AE Title'),
        ),
        migrations.AlterField(
            model_name='dicomserver',
            name='hostname',
            field=models.CharField(help_text='The hostname is just a friendly name used for identifying the server.', max_length=128, unique=True, verbose_name='Hostname (friendly name)'),
        ),
        migrations.AlterField(
            model_name='dicomserver',
            name='ip_address',
            field=models.GenericIPAddressField(default='127.0.0.1', help_text='The IP Address that this DICOM server will listen on (default is localhost 127.0.0.1)', verbose_name='IP Address'),
        ),
        migrations.AlterField(
            model_name='dicomserver',
            name='port',
            field=models.PositiveIntegerField(default=11112, help_text='The port number that this DICOM Server will listen on (default is 11112)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(65536)], verbose_name='Port Number'),
        ),
    ]
