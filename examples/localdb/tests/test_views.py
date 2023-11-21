from django.urls import reverse


def perform_authenticated_reqest(client, token):
    return client.get(reverse("auth"), headers={"Authorization": f"Bearer {token}"})


def test_view_without_auth_success(client):
    response = client.get(reverse("noauth"))
    assert response.status_code == 200
    assert not response.data


def test_view_without_auth_success_with_token(client, access_token, token_payload):
    response = client.get(
        reverse("auth"),
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200
    assert response.data["id"] == token_payload["sub"]


def test_auth_success(client, access_token, token_payload):
    response = perform_authenticated_reqest(client, access_token)
    assert response.status_code == 200
    assert response.data["id"] == token_payload["sub"]


def test_rejected_without_token(client):
    response = client.get(reverse("auth"))
    assert response.status_code == 401


def test_invalid_token_rejected(client):
    response = perform_authenticated_reqest(client, "invalid")
    assert response.status_code == 401


def test_expired_token_rejected(client, expired_access_token):
    response = perform_authenticated_reqest(client, expired_access_token)
    assert response.status_code == 401


def test_anonymous_token_rejected(client, anonymous_access_token):
    response = perform_authenticated_reqest(client, anonymous_access_token)
    assert response.status_code == 401


def test_sign_in_page_available(client):
    response = client.get(reverse("supabase_signin"))
    assert response.status_code == 200
