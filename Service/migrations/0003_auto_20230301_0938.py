# Generated by Django 3.1.7 on 2023-03-01 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Service', '0002_enquire_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquire',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
