from django.db import connection


def test_search_path_set(db):
    with connection.cursor() as cursor:
        cursor.execute("show search_path;")
        result = cursor.fetchone()
        search_path = result[0].split(",")
        expected_path = ["onlydb", "public", "auth", "extensions"]
        assert [path.strip() for path in search_path] == expected_path
