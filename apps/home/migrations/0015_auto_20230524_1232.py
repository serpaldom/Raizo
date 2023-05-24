# Generated by Django 3.2.16 on 2023-05-24 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20230523_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalrule',
            name='severity',
            field=models.IntegerField(choices=[(1, 'Critical'), (2, 'Very High'), (3, 'High'), (4, 'Medium'), (5, 'Low'), (6, 'Informational')], default=1),
        ),
        migrations.AlterField(
            model_name='rule',
            name='severity',
            field=models.IntegerField(choices=[(1, 'Critical'), (2, 'Very High'), (3, 'High'), (4, 'Medium'), (5, 'Low'), (6, 'Informational')], default=1),
        ),
    ]
