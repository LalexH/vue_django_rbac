# Generated by Django 3.1.13 on 2023-07-24 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysmenus',
            name='parent_id',
            field=models.IntegerField(default=0, verbose_name='parent_id'),
        ),
    ]