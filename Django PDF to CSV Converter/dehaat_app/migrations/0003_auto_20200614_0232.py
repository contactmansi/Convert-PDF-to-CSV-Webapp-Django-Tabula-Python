# Generated by Django 2.1.3 on 2020-06-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dehaat_app', '0002_auto_20200613_2254'),
    ]

    operations = [
        migrations.DeleteModel(
            name='file',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount_2015',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount_2016',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]
