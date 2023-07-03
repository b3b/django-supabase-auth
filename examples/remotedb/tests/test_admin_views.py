from supa_auth.tests.factories import SuperUserFactory, UserFactory


def test_admin_login(db, client):
    SuperUserFactory.create(username="admin", password="1234")

    response = client.post("/admin/login/", {"username": "admin", "password": "1234"})

    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated


def test_admin_wrong_password(db, client):
    SuperUserFactory.create(username="admin", password="1234")

    response = client.post(
        "/admin/login/", {"username": "admin", "password": "12341234"}
    )

    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated


def test_nostaff_user_forbidden(db, client):
    UserFactory.create(username="admin", password="1234")

    response = client.post("/admin/login/", {"username": "admin", "password": "1234"})

    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated
