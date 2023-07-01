"""supa_auth.client"""
from django.db.backends.postgresql.client import (
    DatabaseClient as PostgresqlDatabaseClient,
)


class DatabaseClient(PostgresqlDatabaseClient):
    """Database client class for Supabase database.

    This class extends the default PostgreSQL database client class and
    passes extra connection options to the `psql` client.
    Original client do pass connection options from settings to the `psql`.
    """

    @classmethod
    def settings_to_cmd_args_env(
        cls, settings_dict: dict, parameters: dict
    ) -> tuple[list, dict]:
        """
        Convert settings dictionary to command-line arguments
        and environment variables.
        """
        args, env = PostgresqlDatabaseClient.settings_to_cmd_args_env(
            settings_dict, parameters
        )
        env.update(cls.options_from_settings(settings_dict))
        return args, env

    @classmethod
    def options_from_settings(cls, settings_dict: dict) -> dict:
        """
        Extract parameters to use (like `search_path` and `tcp_keepalives_idle`)
        when connecting to the database.
        """
        try:
            options = settings_dict["OPTIONS"]["options"]
        except KeyError:
            return {}
        return {"PGOPTIONS": options}
