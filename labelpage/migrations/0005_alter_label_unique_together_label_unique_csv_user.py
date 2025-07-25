# Generated by Django 4.2.17 on 2025-01-10 22:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_alter_csvdata_csv_file_alter_csvdata_image_filename_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labelpage', '0004_alter_label_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='label',
            unique_together={('csv_data', 'user')},
        ),
        migrations.AddConstraint(
            model_name='label',
            constraint=models.UniqueConstraint(fields=('csv_data', 'user'), name='unique_csv_user'),
        ),
    ]
