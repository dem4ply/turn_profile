# Generated by Django 2.0.7 on 2018-09-03 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Background_check',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='Background check id')),
                ('name', models.CharField(max_length=128)),
                ('adapter', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='Package id')),
                ('name', models.CharField(max_length=128)),
                ('background_checks', models.ManyToManyField(related_name='packages', to='background_check.Background_check')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_packages', to='partners.Partner')),
            ],
        ),
    ]
