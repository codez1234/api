# Generated by Django 4.0.3 on 2022-06-24 13:09

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(db_column='fld_ai_id', primary_key=True, serialize=False)),
                ('version_name', django_mysql.models.FixedCharField(blank=True, db_column='fld_version_name', max_length=10, null=True)),
                ('type', django_mysql.models.EnumField(blank=True, choices=[('android', 'Android'), ('iso', 'Ios')], db_column='fld_type', default='android', null=True)),
                ('is_active', models.BooleanField(db_column='fld_is_active', default=True)),
                ('is_delete', models.BooleanField(db_column='fld_is_delete', default=False)),
                ('created_datetime', models.DateTimeField(blank=True, db_column='fld_created_datetime', null=True)),
            ],
            options={
                'db_table': 'tbl_version_check',
            },
        ),
    ]
