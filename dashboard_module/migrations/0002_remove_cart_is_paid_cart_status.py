# Generated by Django 4.1.1 on 2022-09-22 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_module', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
