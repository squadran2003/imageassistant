# Generated migration for Avatar Creation service

from django.db import migrations


def add_avatar_service(apps, schema_editor):
    Service = apps.get_model('images', 'Service')
    Service.objects.create(
        code=9,
        name='Avatar Creation',
        description='Transform your photo into a stylized AI avatar',
        free=False,
        tokens=5
    )


def reverse_avatar_service(apps, schema_editor):
    Service = apps.get_model('images', 'Service')
    Service.objects.filter(code=9).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0022_add_token_cost_to_services'),
    ]

    operations = [
        migrations.RunPython(add_avatar_service, reverse_avatar_service),
    ]