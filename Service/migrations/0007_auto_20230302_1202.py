# Generated by Django 3.1.7 on 2023-03-02 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Service', '0006_auto_20230302_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='Service.product'),
        ),
    ]
