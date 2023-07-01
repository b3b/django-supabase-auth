"""'supa_auth' app settings."""

# Use separate schema for Django tables
DEFAULT_SCHEMA = "django"
# Limit the maximum lifetime of a connection
DEFAULT_CONN_MAX_AGE = 900
# Enable TCP keepalive message to prevent disconntections
DEFAULT_KEEPALIVES_IDLE = 75
