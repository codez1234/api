# Generated by Django 4.0.3 on 2022-06-23 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_tblrates_fld_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbluserreimbursements',
            name='amount',
            field=models.FloatField(blank=True, db_column='fld_amount', null=True),
        ),
    ]
