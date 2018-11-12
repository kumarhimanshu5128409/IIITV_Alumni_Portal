# Generated by Django 2.1.3 on 2018-11-09 06:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumni',
            name='profile_pic',
        ),
        migrations.AlterField(
            model_name='alumni',
            name='area_of_expertise',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[(A-Z)|(a-z)|(\\s)|(\\-)]+$')]),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='permanent_address',
            field=models.CharField(max_length=700, validators=[django.core.validators.RegexValidator('^[(A-Z)|(a-z)|(0-9)|(\\s)|(\\-)|(\\.)|(,)|(\\:)]+$')]),
        ),
    ]