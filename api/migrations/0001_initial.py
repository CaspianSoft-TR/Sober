# Generated by Django 2.1.5 on 2019-01-28 06:52

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'NEW'), (1, 'ACCEPTED'), (2, 'REJECTED')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField()),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('modelyear', models.IntegerField()),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=20)),
                ('arrival_destination', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_info', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DriverHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=20, verbose_name=api.models.Category)),
                ('arrival_destination', models.CharField(max_length=20, verbose_name=api.models.Category)),
                ('booked_time', models.DateTimeField(auto_now_add=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Customer')),
                ('driver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='DriverLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.CharField(max_length=10)),
                ('latitude', models.CharField(max_length=10)),
                ('location_name', models.CharField(max_length=20)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Category')),
                ('driver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=200)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Customer')),
                ('driver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Customer')),
                ('driver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='TravelHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=20, verbose_name=api.models.Category)),
                ('arrival_destination', models.CharField(max_length=20, verbose_name=api.models.Category)),
                ('booked_time', models.DateTimeField(auto_now_add=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Customer')),
                ('driver_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='UserCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField()),
                ('number_plate', models.CharField(max_length=20)),
                ('color', models.CharField(default='', max_length=100)),
                ('gear_type', models.IntegerField(choices=[(0, 'UNKNOWN'), (1, 'AUTO'), (2, 'MANUAL')], default=2)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Customer'),
        ),
        migrations.AddField(
            model_name='booking',
            name='driver_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Driver'),
        ),
    ]
