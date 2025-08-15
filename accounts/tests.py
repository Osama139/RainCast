import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_signup_page_renders(client):
    r = client.get(reverse("accounts:signup"))
    assert r.status_code == 200

@pytest.mark.django_db
def test_login_page_renders(client):
    r = client.get(reverse("accounts:login"))
    assert r.status_code == 200

@pytest.mark.django_db
def test_signup_creates_user_and_login(client):
    # Sign up
    resp = client.post(reverse("accounts:signup"), data={
        "username": "testuser",
        "password1": "Password123!",
        "password2": "Password123!",
    })
    assert resp.status_code == 302
    assert User.objects.filter(username="testuser").exists()

    # Login using the same credentials
    resp2 = client.post(reverse("accounts:login"), data={
        "username": "testuser",
        "password": "Password123!",
    })
    assert resp2.status_code == 302
    assert "_auth_user_id" in client.session