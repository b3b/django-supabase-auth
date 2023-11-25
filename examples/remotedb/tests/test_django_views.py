from django.urls import reverse

from supa_auth.tests.factories import UserFactory


def perform_authenticated_reqest(client, token):
    return client.post(
        reverse("login_with_jwt"), headers={"Authorization": f"Bearer {token}"}
    )


def test_login_required_passed(db, client):
    user = UserFactory.create(password="1234")
    client.force_login(user)

    response = client.post(reverse("login_with_jwt"))

    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated
    assert response.content.decode() == ""


def test_login_required_passed_with_access_token(
    db, client, token_payload, access_token
):
    user = UserFactory.create(id=token_payload["sub"])
    user.refresh_from_db()

    response = perform_authenticated_reqest(client, access_token)

    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated
    assert response.wsgi_request.user == user
    assert response.content.decode() == ""


def test_login_required_forbidden_with_unknown_user_access_token(
    db, client, access_token
):
    response = perform_authenticated_reqest(client, access_token)

    assert response.status_code == 401
    assert not response.wsgi_request.user.is_authenticated


def test_login_required_forbidden(db, client):
    response = client.post(reverse("login_with_jwt"))

    assert response.status_code == 401
    assert not response.wsgi_request.user.is_authenticated
