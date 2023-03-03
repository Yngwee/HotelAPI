# Generated by Django 4.1.6 on 2023-03-02 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_rename_users_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='isBooked',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.FloatField(default=1000),
            preserve_default=False,
        ),
    ]