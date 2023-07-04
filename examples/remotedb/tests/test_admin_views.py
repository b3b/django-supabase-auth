import pytest

from supa_auth.tests.factories import SuperUserFactory, UserFactory


def test_admin_login(db, client):
    uid = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    SuperUserFactory.create(id=uid, password="1234")

    response = client.post("/admin/login/", {"username": uid, "password": "1234"})
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated


def test_admin_wrong_password(db, client):
    uid = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    SuperUserFactory.create(id=uid, password="1234")

    response = client.post("/admin/login/", {"username": uid, "password": "12341234"})

    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.skip("todo: implement `is_staff` logic")
def test_nostaff_user_forbidden(db, client):
    uid = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    UserFactory.create(id=uid, password="1234")

    response = client.post("/admin/login/", {"username": uid, "password": "1234"})

    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated
