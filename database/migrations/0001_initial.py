# Generated by Django 4.0.3 on 2022-06-05 20:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audittrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('script', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.CharField(blank=True, max_length=255, null=True)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('table', models.CharField(blank=True, max_length=255, null=True)),
                ('field', models.CharField(blank=True, max_length=255, null=True)),
                ('keyvalue', models.TextField(blank=True, null=True)),
                ('oldvalue', models.TextField(blank=True, null=True)),
                ('newvalue', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'audittrail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=255, null=True)),
                ('endpoint', models.TextField()),
                ('publickey', models.CharField(max_length=255)),
                ('authenticationtoken', models.CharField(max_length=255)),
                ('contentencoding', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'subscriptions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblAdmin',
            fields=[
                ('fld_ai_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fld_name', models.CharField(blank=True, max_length=100, null=True)),
                ('fld_username', models.CharField(blank=True, max_length=100, null=True)),
                ('fld_password', models.CharField(blank=True, max_length=255, null=True)),
                ('fld_created_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tbl_admin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblRates',
            fields=[
                ('fld_ai_id', models.AutoField(primary_key=True, serialize=False)),
                ('fld_state', models.CharField(blank=True, max_length=50, null=True)),
                ('fld_rate', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('fld_is_active', models.BooleanField(default=True)),
                ('fld_created_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tbl_rates',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblSites',
            fields=[
                ('id', models.AutoField(db_column='fld_ai_id', primary_key=True, serialize=False)),
                ('site_omc_id', models.CharField(blank=True, db_column='fld_site_omc_id', max_length=10, null=True)),
                ('site_type', models.CharField(blank=True, db_column='fld_site_type', max_length=6, null=True)),
                ('site_name', models.CharField(blank=True, db_column='fld_site_name', max_length=100, null=True)),
                ('state', models.CharField(blank=True, db_column='fld_state', max_length=50, null=True)),
                ('district', models.CharField(blank=True, db_column='fld_district', max_length=100, null=True)),
                ('latitude', models.CharField(blank=True, db_column='fld_latitude', max_length=100, null=True)),
                ('longitude', models.CharField(blank=True, db_column='fld_longitude', max_length=100, null=True)),
                ('is_active', models.BooleanField(db_column='fld_is_active', default=True)),
                ('is_delete', models.BooleanField(db_column='fld_is_delete', default=False)),
                ('created_datetime', models.DateField(auto_now_add=True, db_column='fld_created_datetime')),
            ],
            options={
                'db_table': 'tbl_sites',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblUserLevel',
            fields=[
                ('fld_ai_id', models.AutoField(primary_key=True, serialize=False)),
                ('fld_user_level_name', models.CharField(blank=True, max_length=20, null=True)),
                ('fld_is_active', models.BooleanField(default=True)),
                ('fld_created_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tbl_user_level',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblUserSites',
            fields=[
                ('id', models.AutoField(db_column='fld_ai_id', primary_key=True, serialize=False)),
                ('assigned_date', models.DateTimeField(blank=True, db_column='fld_assigned_date', null=True)),
                ('is_active', models.BooleanField(db_column='fld_is_active', default=True)),
                ('is_delete', models.BooleanField(db_column='fld_is_delete', default=False)),
                ('created_datetime', models.DateTimeField(auto_now_add=True, db_column='fld_created_datetime')),
                ('sites', models.ManyToManyField(db_column='fld_sites', to='database.tblsites')),
                ('user_id', models.ForeignKey(blank=True, db_column='fld_user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_user_sites',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblUserReimbursements',
            fields=[
                ('id', models.AutoField(db_column='fld_ai_id', primary_key=True, serialize=False)),
                ('claim_id', models.CharField(blank=True, db_column='fld_claim_id', max_length=100, null=True)),
                ('visit_id', models.CharField(blank=True, db_column='fld_visit_id', max_length=50, null=True)),
                ('distance', models.FloatField(blank=True, db_column='fld_distance', null=True)),
                ('amount', models.IntegerField(blank=True, db_column='fld_amount', null=True)),
                ('status', models.CharField(blank=True, choices=[('approved', 'approved'), ('pending', 'pending'), ('requested', 'requested'), ('closed', 'closed')], db_column='fld_status', default='pending', max_length=20, null=True)),
                ('is_active', models.BooleanField(db_column='fld_is_active', default=True)),
                ('is_delete', models.BooleanField(db_column='fld_is_delete', default=False)),
                ('date', models.DateField(blank=True, db_column='fld_date', null=True)),
                ('created_datetime', models.DateTimeField(blank=True, db_column='fld_created_datetime', null=True)),
                ('user_id', models.ForeignKey(blank=True, db_column='fld_user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_user_reimbursements',
            },
        ),
        migrations.CreateModel(
            name='TblUserDevices',
            fields=[
                ('fld_ai_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fld_device_model', models.CharField(blank=True, max_length=100, null=True)),
                ('fld_imei_1', models.CharField(blank=True, max_length=100, null=True)),
                ('fld_imei_2', models.CharField(blank=True, max_length=100, null=True)),
                ('fld_device_id_token', models.CharField(blank=True, max_length=255, null=True)),
                ('fld_is_active', models.BooleanField(default=True)),
                ('fld_created_datetime', models.DateTimeField(auto_now_add=True)),
                ('fld_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_user_devices',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TblAttendanceLog',
            fields=[
                ('id', models.AutoField(db_column='fld_ai_id', primary_key=True, serialize=False)),
                ('visit_id', models.CharField(blank=True, db_column='fld_visit_id', max_length=50, null=True)),
                ('start_latitude', models.FloatField(blank=True, db_column='fld_start_latitude', null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('start_longitude', models.FloatField(blank=True, db_column='fld_start_longitude', null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('end_latitude', models.FloatField(blank=True, db_column='fld_end_latitude', null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('end_longitude', models.FloatField(blank=True, db_column='fld_end_longitude', null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('start_time', models.TimeField(blank=True, db_column='fld_start_time', null=True)),
                ('end_time', models.TimeField(blank=True, db_column='fld_end_time', null=True)),
                ('date', models.DateField(blank=True, db_column='fld_date', null=True)),
                ('is_active', models.BooleanField(db_column='fld_is_active', default=True)),
                ('is_delete', models.BooleanField(db_column='fld_is_delete', default=False)),
                ('created_datetime', models.DateTimeField(blank=True, db_column='fld_created_datetime', null=True)),
                ('site_id', models.ForeignKey(blank=True, db_column='fld_site_omc_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.tblsites')),
                ('user_id', models.ForeignKey(blank=True, db_column='fld_user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_attendance_log',
            },
        ),
        migrations.CreateModel(
            name='TblAttendance',
            fields=[
                ('fld_ai_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fld_attendance_status', models.CharField(blank=True, choices=[('check_in', 'check_in'), ('current', 'current'), ('check_out', 'check_out')], max_length=9, null=True)),
                ('fld_latitude', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('fld_longitude', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('fld_device_info', models.CharField(blank=True, max_length=100, null=True)),
                ('fld_ip_address', models.CharField(blank=True, max_length=100, null=True)),
                ('visit_id', models.CharField(blank=True, db_column='fld_visit_id', max_length=50, null=True)),
                ('fld_is_active', models.BooleanField(default=True)),
                ('fld_is_delete', models.BooleanField(default=False)),
                ('fld_date', models.DateField(blank=True, null=True)),
                ('fld_time', models.TimeField(blank=True, null=True)),
                ('fld_created_datetime', models.DateTimeField(auto_now_add=True)),
                ('fld_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_attendance',
                'managed': True,
            },
        ),
    ]
