# Generated by Django 4.1.7 on 2023-04-07 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Service', '0004_scheduleservice_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdiscounts', to='Service.product'),
        ),
    ]