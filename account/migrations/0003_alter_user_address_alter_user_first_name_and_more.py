# Generated by Django 4.0.3 on 2022-06-16 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, db_column='fld_address', default=' ', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, db_column='fld_first_name', default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, db_column='fld_last_name', default=' ', max_length=100, null=True),
        ),
    ]