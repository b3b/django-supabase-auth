"""'supa_auth' app settings."""
import datetime

from django.utils import timezone

# Use separate schema for Django tables
DEFAULT_SCHEMA = "django"
# Limit the maximum lifetime of a connection
DEFAULT_CONN_MAX_AGE = 900
# Enable TCP keepalive message to prevent disconntections
DEFAULT_KEEPALIVES_IDLE = 75

DEFAULT_APP_METADATA = {"provider": "email", "providers": ["email"]}
BAN_FOREVER_TIME = timezone.datetime(3000, 12, 31, tzinfo=datetime.timezone.utc)
