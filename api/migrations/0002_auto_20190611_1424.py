# Generated by Django 2.1.5 on 2019-06-11 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='room_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.CharField(default=0, max_length=55),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.CharField(default=0, max_length=55),
        ),
        migrations.AlterField(
            model_name='address',
            name='title',
            field=models.CharField(max_length=55),
        ),
    ]
