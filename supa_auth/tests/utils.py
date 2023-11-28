from typing import Container

from django.db import connection


def sql_select_to_dict(sql_query: str) -> dict | None:
    """Executes an SQL query and returns the first result row as a dictionary."""
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            row_dict = dict(zip(columns, row))
            return row_dict
    return None


def dict_diff(d1: dict, d2: dict, ignored_fields: Container | None = None) -> dict:
    """Compares two dictionaries and returns the differences as a dictionary."""
    ignored_fields = ignored_fields or set()
    return {
        k: (d1.get(k), d2.get(k))
        for k in (set(d1) | set(d2))
        if d1[k] != d2[k] and k not in ignored_fields
    }
