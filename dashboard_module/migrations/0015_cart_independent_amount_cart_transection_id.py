# Generated by Django 4.1.1 on 2022-09-27 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_module', '0014_remove_userdiscountcode_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='Independent_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='transection_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]