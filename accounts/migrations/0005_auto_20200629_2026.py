# Generated by Django 3.0.7 on 2020-06-29 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customer_profile_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='profile_pic',
            new_name='profile_picture',
        ),
    ]
