# Generated by Django 4.0.5 on 2024-02-12 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fatigue_Detection_App', '0003_worker_device_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='device_token',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
