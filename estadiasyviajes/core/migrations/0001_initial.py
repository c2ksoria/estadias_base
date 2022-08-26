# Generated by Django 4.1 on 2022-08-26 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Commercial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CommercialName', models.CharField(max_length=50, verbose_name='Name')),
                ('lat', models.DecimalField(decimal_places=8, max_digits=10, verbose_name='Latitude')),
                ('lng', models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Longitude')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('CommercialEmail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StatusName', models.CharField(max_length=50, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='SocialNetworksGlobal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SocialName', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status', verbose_name='SocialName')),
            ],
        ),
        migrations.CreateModel(
            name='Propietary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('Status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status', verbose_name='Status')),
                ('User', models.OneToOneField(max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Propietaries',
            },
        ),
    ]
