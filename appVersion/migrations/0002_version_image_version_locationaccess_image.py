# Generated by Django 4.0.3 on 2022-06-30 14:56

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('appVersion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='image',
            field=models.ImageField(blank=True, db_column='fld_image', null=True, upload_to='', verbose_name='images'),
        ),
        migrations.AddField(
            model_name='version',
            name='locationaccess_image',
            field=django_mysql.models.FixedCharField(blank=True, db_column='fld_locationaccess_image', max_length=30, null=True),
        ),
    ]