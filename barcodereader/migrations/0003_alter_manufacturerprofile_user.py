# Generated by Django 5.1.6 on 2025-03-15 10:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcodereader', '0002_manufacturerprofile_business_licence'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturerprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturer_profiles', to=settings.AUTH_USER_MODEL),
        ),
    ]
