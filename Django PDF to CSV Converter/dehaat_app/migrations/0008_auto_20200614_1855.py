# Generated by Django 2.1.3 on 2020-06-14 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dehaat_app', '0007_auto_20200614_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='particulars',
            field=models.CharField(max_length=100),
        ),
    ]
