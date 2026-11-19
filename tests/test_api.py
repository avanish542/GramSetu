import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_drf_api_endpoints(client):
    res_projects = client.get('/api/projects/')
    assert res_projects.status_code == 200
    assert 'results' in res_projects.json()

    res_services = client.get('/api/services/')
    assert res_services.status_code == 200

    res_schemes = client.get('/api/schemes/')
    assert res_schemes.status_code == 200

    res_infra = client.get('/api/infrastructure/')
    assert res_infra.status_code == 200
