# Generated by Django 2.0.1 on 2019-05-08 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logintracker',
            name='log_in',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='logintracker',
            name='log_out',
            field=models.DateTimeField(auto_now=True),
        ),
    ]