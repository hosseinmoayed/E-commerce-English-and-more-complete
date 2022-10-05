# Generated by Django 4.1.1 on 2022-09-24 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard_module', '0005_rename_discount_codes_discountcodes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discountcodes',
            name='user',
        ),
        migrations.CreateModel(
            name='UserDiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard_module.discountcodes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
