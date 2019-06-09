# Generated by Django 2.1.5 on 2019-06-09 00:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190607_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='phone',
        ),
        migrations.AlterField(
            model_name='driver',
            name='driver_license',
            field=models.ImageField(blank=True, upload_to='documents'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='national_id',
            field=models.ImageField(blank=True, upload_to='documents'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userinfo', to=settings.AUTH_USER_MODEL),
        ),
    ]
