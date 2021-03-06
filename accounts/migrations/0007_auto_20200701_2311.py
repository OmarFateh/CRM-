# Generated by Django 3.0.7 on 2020-07-01 21:11

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200629_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='picture',
            field=models.ImageField(blank=True, default='profile_pics/2.png', null=True, upload_to=accounts.models.profile_pic_upload),
        ),
    ]
