# Generated by Django 3.1.7 on 2023-03-01 09:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(default='none', max_length=20)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='photos/logos')),
                ('liscences', models.ImageField(blank=True, null=True, upload_to='photos/liscences')),
                ('phone_number', models.CharField(max_length=10)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/Businesses')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='businesses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='photos/profiles')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15)),
                ('neccesary_info', models.TextField(max_length=200)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('category', models.TextField(choices=[(1, 'political'), (2, 'entertainment'), (3, 'promotion')], max_length=100)),
                ('description', models.TextField(max_length=200)),
                ('organizers', models.CharField(max_length=50)),
                ('hosts', models.CharField(max_length=50)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.business')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=200)),
                ('message', models.TextField(max_length=500)),
                ('category', models.TextField(max_length=200)),
                ('date', models.DateField()),
                ('outlet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.business')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('charges', models.DecimalField(decimal_places=2, max_digits=6)),
                ('quantity', models.PositiveIntegerField()),
                ('images', models.FileField(blank=True, null=True, upload_to='photo/Service')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos')),
                ('description', models.TextField(max_length=200)),
                ('business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='Service.business')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('charges', models.DecimalField(decimal_places=2, max_digits=6)),
                ('images', models.FileField(blank=True, null=True, upload_to='photo/Service')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos')),
                ('description', models.TextField(max_length=200)),
                ('business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='Service.business')),
            ],
        ),
        migrations.CreateModel(
            name='Testimony',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testimony', models.TextField(max_length=200)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.business')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.customer')),
            ],
            options={
                'verbose_name': 'Testimony',
            },
        ),
        migrations.CreateModel(
            name='StateService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField()),
                ('description', models.TextField(blank=True, max_length=50, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.service')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.service')),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total_price', models.CharField(max_length=15)),
                ('time', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='Service.product')),
            ],
        ),
        migrations.CreateModel(
            name='ReferService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referee', models.CharField(max_length=30)),
                ('message', models.TextField(default='none', max_length=50)),
                ('refered', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.service')),
            ],
        ),
        migrations.CreateModel(
            name='RateService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField()),
                ('comment', models.TextField(max_length=200)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.service')),
            ],
        ),
        migrations.CreateModel(
            name='RateBusiness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField()),
                ('comment', models.TextField(max_length=200)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.business')),
            ],
        ),
        migrations.CreateModel(
            name='Patronage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField()),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.business')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.customer')),
            ],
        ),
        migrations.CreateModel(
            name='NewsLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reads', models.PositiveIntegerField()),
                ('likes', models.PositiveIntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.news')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed', models.TextField(max_length=200)),
                ('bussiness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.service')),
            ],
        ),
        migrations.CreateModel(
            name='EventLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50)),
                ('google_map', models.URLField(blank=True, null=True)),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Service.event')),
            ],
        ),
        migrations.CreateModel(
            name='EnquiryResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField(max_length=200)),
                ('time', models.DateTimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Enquire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enquiry', models.CharField(max_length=200)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enquiries', to='Service.business')),
            ],
        ),
        migrations.CreateModel(
            name='DiscountService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField()),
                ('duration', models.DurationField()),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Service.service')),
            ],
        ),
        migrations.CreateModel(
            name='DiscountProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('duration', models.DurationField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.product')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery_men',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Service.business')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Service.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.business')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.customer')),
                ('d_man', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.sales')),
            ],
        ),
        migrations.CreateModel(
            name='Dealings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dealing_list', models.CharField(default='selling', max_length=50)),
                ('dealings', models.TextField(max_length=1000)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service.business')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_map', models.URLField(blank=True, null=True)),
                ('county', models.CharField(max_length=15)),
                ('sub_county', models.CharField(max_length=15, null=True)),
                ('local_town', models.CharField(max_length=15, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='Service.customer')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county', models.CharField(default='meru', max_length=15)),
                ('sub_county', models.CharField(default='nchiru', max_length=15)),
                ('local_town', models.CharField(default='nchiru', max_length=15)),
                ('google_map', models.URLField(blank=True, null=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='Service.business')),
            ],
        ),
    ]