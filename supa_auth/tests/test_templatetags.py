from django.template import Context, Template


def test_supabase_client_created_by_tag():
    out = Template("{% load supa_auth %}{% supabase_client %}").render(Context())
    assert "@supabase/supabase-js" in out
    assert "supabase.createClient" in out
