# Generated by Django 4.0.4 on 2022-07-12 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_dicomserver_output_directory'),
    ]

    operations = [
        migrations.CreateModel(
            name='SOPInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=64)),
                ('study_uid', models.CharField(max_length=64)),
                ('series_uids', models.CharField(max_length=64)),
            ],
        ),
    ]
