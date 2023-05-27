# Generated by Django 3.2.16 on 2023-05-26 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_userpreferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='reports', to='home.Tag'),
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='theme_preference',
            field=models.CharField(choices=[('dark', 'Dark'), ('light', 'Light')], default='dark', max_length=20),
        ),
        migrations.AlterField(
            model_name='watcher',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='watchers', to='home.Tag'),
        ),
    ]