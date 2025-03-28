# Generated by Django 5.1.6 on 2025-03-25 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcodereader', '0011_alter_counterfeit_report_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='counterfeit_report',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='counterfeit_report',
            name='resolved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
