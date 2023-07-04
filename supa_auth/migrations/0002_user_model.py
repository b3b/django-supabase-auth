# pylint: disable=missing-docstring
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("supa_auth", "0001_initial"),
    ]
    run_before = [
        ("auth", "__first__"),
        ("admin", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="SupaUser",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": '"auth"."users"',
                "managed": False,
            },
        ),
    ]
