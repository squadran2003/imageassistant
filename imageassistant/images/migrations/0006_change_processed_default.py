# Generated by Django 4.2.15 on 2024-08-21 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_remove_upload_to_files_dir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]