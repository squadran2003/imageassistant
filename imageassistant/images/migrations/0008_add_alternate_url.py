# Generated by Django 4.2.16 on 2024-10-08 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_increae_image_filename_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='alternate_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]