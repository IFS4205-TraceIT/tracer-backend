# Generated by Django 4.1 on 2022-09-10 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infections', '0003_remove_notifications_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infectionhistory',
            name='has_uploaded',
        ),
    ]