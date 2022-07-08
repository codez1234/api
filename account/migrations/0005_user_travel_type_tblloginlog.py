# Generated by Django 4.0.3 on 2022-07-08 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_alter_tbluserreimbursements_amount'),
        ('account', '0004_alter_user_address_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='travel_type',
            field=models.ForeignKey(blank=True, db_column='fld_travel_type', null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.tblrates'),
        ),
        migrations.CreateModel(
            name='TblLoginLog',
            fields=[
                ('fld_ai_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fld_type', models.CharField(default='other', max_length=6)),
                ('fld_app', models.CharField(default='mobileapp', max_length=9)),
                ('fld_access_token', models.TextField(blank=True, null=True)),
                ('fld_device', models.CharField(blank=True, max_length=100, null=True)),
                ('fld_device_information', models.TextField(blank=True, null=True)),
                ('fld_ip_address', models.CharField(blank=True, max_length=100, null=True)),
                ('fld_is_active', models.BooleanField(default=True)),
                ('fld_is_delete', models.BooleanField(default=False)),
                ('fld_created_datetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('fld_user_id', models.ForeignKey(blank=True, db_column='fld_user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_login_log',
                'managed': True,
            },
        ),
    ]
