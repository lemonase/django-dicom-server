# Generated by Django 4.0.4 on 2022-07-12 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_sopinstance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicomserver',
            name='ip_address',
            field=models.GenericIPAddressField(default='0.0.0.0', help_text='The IP Address that this DICOM server will listen on (default is 0.0.0.0 to listen externally on all IP Addresses).', verbose_name='IP Address'),
        ),
    ]
