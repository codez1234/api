# Generated by Django 4.0.3 on 2022-06-22 11:24

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_tblpushnotificationlog_firebase_response_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbluserfirebase',
            name='firebase_id',
            field=django_mysql.models.FixedCharField(blank=True, db_column='fld_firebase_id', default='NA', max_length=255, null=True),
        ),
    ]
