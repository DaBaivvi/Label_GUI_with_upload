# Generated by Django 4.2.17 on 2025-01-10 13:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labelpage', '0002_alter_label_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='label',
            unique_together={('csv_data', 'user')},
        ),
    ]
