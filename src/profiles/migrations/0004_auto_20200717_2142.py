# Generated by Django 3.0.8 on 2020-07-17 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20200716_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='status',
            field=models.CharField(choices=[('accepted', 'accepted'), ('sent', 'sent')], max_length=8),
        ),
    ]
