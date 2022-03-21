# Generated by Django 4.0.2 on 2022-03-20 05:27

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='phoneModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('isVerified', models.BooleanField(default=False)),
                ('counter', models.IntegerField(default=0)),
            ],
        ),
    ]