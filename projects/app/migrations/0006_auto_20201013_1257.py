# Generated by Django 3.0.7 on 2020-10-13 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20201013_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='date_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения аукциона'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='date_start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата начала аукциона'),
        ),
    ]