import pytest
from django.urls import reverse
from apps.accounts.models import User, UserRole

@pytest.mark.django_db
def test_user_roles_and_properties():
    villager = User.objects.create_user(username="test_villager", password="password123", role=UserRole.VILLAGER)
    admin = User.objects.create_user(username="test_admin", password="password123", role=UserRole.PANCHAYAT_ADMIN)

    assert villager.is_villager is True
    assert villager.is_panchayat_admin is False
    assert admin.is_panchayat_admin is True

@pytest.mark.django_db
def test_health_and_ready_endpoints(client):
    res_health = client.get(reverse('core:health'))
    assert res_health.status_code == 200
    assert res_health.json()['status'] == 'healthy'

    res_ready = client.get(reverse('core:ready'))
    assert res_ready.status_code == 200
    assert res_ready.json()['status'] == 'ready'
