from django.urls import reverse

from supa_auth.tests.factories import UserFactory


def test_login_required_passed(db, client):
    user = UserFactory.create(password="1234")
    client.force_login(user)

    response = client.get(reverse("django_login_required"))

    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated
    assert response.content.decode() == f"{user.pk}"


def test_login_required_forbidden(db, client):
    response = client.get(reverse("django_login_required"))

    assert response.status_code == 302
    assert not response.wsgi_request.user.is_authenticated
