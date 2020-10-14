# Generated by Django 3.0.7 on 2020-10-13 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20201013_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratemember',
            name='auction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rate_member', related_query_name='rate_member', to='app.Auction'),
        ),
    ]
