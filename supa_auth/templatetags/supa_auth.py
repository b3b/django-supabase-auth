"""'supa_auth' app template tags."""
from django import template
from django.conf import settings

from supa_auth import settings as app_settings

register = template.Library()


@register.inclusion_tag("supa_auth/supabase_client.html")
def supabase_client():
    """Include the configured Supabase client instance ('supabase' variable)
    within the template.

    Usage:
        {% load supa_auth %}
        {% supabase_client %}
        <script>
        supabase.auth.getSession();
        </script>
    """
    return {
        "supabase_script_url": app_settings.SUPABASE_SCRIPT_URL,
        "supabase_url": settings.SUPABASE_URL,
        "supabase_key": settings.SUPABASE_API_KEY,
    }
