# Generated by Django 3.0.3 on 2020-03-09 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200310_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(default='Unknown', max_length=20),
        ),
    ]