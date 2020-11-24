# Generated by Django 3.0.7 on 2020-11-09 01:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201109_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailactivation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL),
        ),
    ]