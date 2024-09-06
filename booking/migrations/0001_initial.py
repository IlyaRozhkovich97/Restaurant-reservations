# Generated by Django 5.1 on 2024-08-30 14:15

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название зала')),
            ],
            options={
                'verbose_name': 'Зал',
                'verbose_name_plural': 'Залы',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('guests', models.IntegerField(verbose_name='Количество гостей')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Телефон')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Комментарии')),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=7200), verbose_name='Продолжительность')),
                ('customer_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('hall', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='booking.hall', verbose_name='Зал')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер стола')),
                ('capacity', models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(6)], verbose_name='Вместимость')),
                ('hall', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='booking.hall', verbose_name='Зал')),
                ('reservations', models.ManyToManyField(blank=True, related_name='related_tables', to='booking.booking', verbose_name='Бронирования')),
            ],
            options={
                'verbose_name': 'Стол',
                'verbose_name_plural': 'Столы',
                'ordering': ['number'],
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='tables',
            field=models.ManyToManyField(blank=True, related_name='related_reservations', to='booking.table', verbose_name='Столы'),
        ),
    ]
