# Generated by Django 4.0.3 on 2022-06-30 15:36

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('appVersion', '0002_version_image_version_locationaccess_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='locationaccess_image',
            field=django_mysql.models.FixedCharField(blank=True, db_column='fld_locationaccess_image', max_length=50, null=True),
        ),
    ]
