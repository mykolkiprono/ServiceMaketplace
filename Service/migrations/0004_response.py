# Generated by Django 3.1.7 on 2023-03-02 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Service', '0003_auto_20230301_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField(max_length=200)),
                ('time', models.DateTimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.service')),
            ],
        ),
    ]
