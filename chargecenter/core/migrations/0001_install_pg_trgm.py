from django.db import migrations


def create_third_party_extension(apps, schema_editor):
    schema_editor.execute("CREATE EXTENSION pg_trgm;")


def drop_third_party_extension(apps, schema_editor):
    schema_editor.execute("DROP EXTENSION IF EXISTS pg_trgm;")


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(create_third_party_extension, reverse_code=drop_third_party_extension, atomic=True)
    ]
