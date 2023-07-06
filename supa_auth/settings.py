"""'supa_auth' app settings."""
import datetime
import uuid

from django.utils import timezone

# Use separate schema for Django tables
DEFAULT_SCHEMA = "django"
# Limit the maximum lifetime of a connection
DEFAULT_CONN_MAX_AGE = 900
# Enable TCP keepalive message to prevent disconntections
DEFAULT_KEEPALIVES_IDLE = 75

DEFAULT_AUDIENCE = "authenticated"
DEFAULT_APP_METADATA = {"provider": "email", "providers": ["email"]}
DEFAULT_INSTANCE_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")
DEFAULT_ROLE = "authenticated"
BAN_FOREVER_TIME = timezone.datetime(3000, 12, 31, tzinfo=datetime.timezone.utc)
