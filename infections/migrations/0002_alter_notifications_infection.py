# Generated by Django 4.1 on 2022-09-10 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infections', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='infection',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='infections.infectionhistory'),
        ),
    ]
