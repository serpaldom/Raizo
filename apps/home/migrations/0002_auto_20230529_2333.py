# Generated by Django 3.2.16 on 2023-05-29 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exceptions',
            options={'verbose_name_plural': 'Exceptions'},
        ),
        migrations.AlterModelOptions(
            name='userpreferences',
            options={'verbose_name_plural': 'User Preferences'},
        ),
    ]