"""Tests that are using Supabase API.
"""
# pylint: disable=no-member
import pytest
from django.conf import settings
from requests_toolbelt import sessions

from supa_auth.models import SupaUser


@pytest.fixture
def supa_client():
    session = sessions.BaseUrlSession(base_url=settings.SUPABASE_URL)
    session.headers = {"apikey": settings.SUPABASE_API_KEY}
    yield session


@pytest.fixture
def live_user_credentials():
    yield {"email": "live-test-user@example.com", "password": "Tb46d4aeaXa08"}


@pytest.fixture
def delete_live_user(live_user_credentials):
    email = live_user_credentials["email"]
    SupaUser.objects.filter(email=email).delete()
    yield
    SupaUser.objects.filter(email=email).delete()


@pytest.fixture
def live_user(delete_live_user, live_user_credentials):
    user = SupaUser.objects.create(email=live_user_credentials["email"])
    yield user


def test_supabase_auth_api_ready_for_tests(supa_client):
    response = supa_client.get("/auth/v1/settings")
    response.raise_for_status()
    data = response.json()
    assert not data["disable_signup"]
    assert data["mailer_autoconfirm"]
    external = data["external"]
    assert external["email"]
    assert external["github"]


@pytest.mark.livedb
@pytest.mark.django_db(transaction=True)
def test_access_granted_after_signup(
    delete_live_user, live_user_credentials, supa_client
):
    assert not SupaUser.objects.filter(email=live_user_credentials["email"]).exists()
    assert supa_client.get("/auth/v1/user").status_code == 401

    response = supa_client.post("/auth/v1/signup", json=live_user_credentials)
    response.raise_for_status()
    access_token = response.json()["access_token"]

    SupaUser.objects.get(email=live_user_credentials["email"])

    supa_client.cookies.clear()
    response = supa_client.post(
        "/auth/v1/token?grant_type=password", json=live_user_credentials
    )
    response.raise_for_status()

    supa_client.headers["Authorization"] = f"Bearer {access_token}"
    response = supa_client.get("/auth/v1/user")
    response.raise_for_status()


@pytest.mark.livedb
@pytest.mark.django_db(transaction=True)
def test_wrong_password_access_prohibited_after_signup(
    delete_live_user, live_user_credentials, supa_client
):
    response = supa_client.post("/auth/v1/signup", json=live_user_credentials)
    response.raise_for_status()

    supa_client.cookies.clear()
    response = supa_client.post(
        "/auth/v1/token?grant_type=password",
        json={"email": live_user_credentials["email"], "password": "wrong-password"},
    )
    assert response.status_code == 400
