# Generated by Django 2.1.3 on 2018-11-09 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0005_auto_20181109_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni',
            name='profile_pic',
            field=models.ImageField(blank=True, default='static_cdn/media_root/default_profile_pic.png', upload_to='media'),
        ),
    ]