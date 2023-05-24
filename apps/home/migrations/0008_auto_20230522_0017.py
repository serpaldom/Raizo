# Generated by Django 3.2.16 on 2023-05-21 22:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_auto_20230522_0015'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HistoricalTechnology',
            new_name='HistoricalTechnologies',
        ),
        migrations.RenameModel(
            old_name='Technology',
            new_name='Technologies',
        ),
        migrations.AlterModelOptions(
            name='historicaltechnologies',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical technologies', 'verbose_name_plural': 'historical technologiess'},
        ),
    ]