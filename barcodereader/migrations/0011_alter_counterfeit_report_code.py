# Generated by Django 5.1.6 on 2025-03-24 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcodereader', '0010_counterfeit_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counterfeit_report',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
