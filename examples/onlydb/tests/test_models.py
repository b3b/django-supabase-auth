import pytest
from django.db import connection
from onlydb.models import Private, Public


@pytest.mark.parametrize(
    "table_name,expected_schema",
    (
        ("onlydb_private", "onlydb"),
        ("onlydb_published", "public"),
    ),
)
def test_table_created_under_expected_schema(db, table_name, expected_schema):
    with connection.cursor() as cursor:
        cursor.execute(
            (
                "select table_schema from information_schema.tables "
                "where table_name=%s"
            ),
            [table_name],
        )
        assert cursor.fetchall() == [(expected_schema,)]


@pytest.mark.parametrize("model", (Private, Public))
def test_django_model_object_created(db, model):
    assert model.objects.count() == 0
    model().save()
    assert model.objects.count() == 1
