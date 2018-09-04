# Generated by Django 2.0.7 on 2018-09-03 16:33

from django.db import migrations


def add_package( apps, schema_editor ):
    from background_check.models import Background_check
    Background_check.objects.create(
        name='validate ssn', adapter='bgc.us_one_validate' )
    Background_check.objects.create(
        name='addresses', adapter='bgc.us_one_trace' )


class Migration(migrations.Migration):

    dependencies = [
        ( 'background_check', '0001_initial' ),
    ]

    operations = [
        migrations.RunPython( add_package ),
    ]
