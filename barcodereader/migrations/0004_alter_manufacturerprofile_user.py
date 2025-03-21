# Generated by Django 5.1.6 on 2025-03-15 11:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcodereader', '0003_alter_manufacturerprofile_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturer_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
