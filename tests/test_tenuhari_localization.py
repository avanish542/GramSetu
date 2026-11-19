import pytest
from django.urls import reverse
from apps.village.models import Village, Ward, VillageInfo, VillageCondition, RelatedPanchayat

@pytest.fixture
def village(db):
    return Village.objects.create(
        name="Tenuhari (Shukla)",
        gram_panchayat="Tenuhari (Shukla) Gram Panchayat",
        block="Sahjanwa",
        district="Gorakhpur",
        state="Uttar Pradesh",
        pincode="273209",
        population=5800,
        households=950,
        total_wards=6
    )

@pytest.mark.django_db
def test_tenuhari_village_model_creation(village):
    assert village.name == "Tenuhari (Shukla)"
    assert village.gram_panchayat == "Tenuhari (Shukla) Gram Panchayat"
    assert village.block == "Sahjanwa"
    assert village.district == "Gorakhpur"
    assert village.state == "Uttar Pradesh"
    assert village.pincode == "273209"

@pytest.mark.django_db
def test_village_conditions(village):
    condition = VillageCondition.objects.create(
        village=village,
        category="Roads",
        condition_status="GOOD",
        description="Paved CC roads across main thoroughfares.",
        remarks="Ward 4 paver block work planned",
        source="Sample Assessment",
        verified=False
    )
    assert condition.get_condition_status_display() == "Good / Satisfactory"
    assert condition.village == village
    assert condition.remarks == "Ward 4 paver block work planned"

@pytest.mark.django_db
def test_unknown_condition_status(village):
    condition = VillageCondition.objects.create(
        village=village,
        category="Water Bodies",
        condition_status="UNKNOWN",
        description="Pond survey unverified.",
        source="Unverified",
        verified=False
    )
    assert condition.get_condition_status_display() == "Unknown / Unverified"

@pytest.mark.django_db
def test_related_panchayats():
    rel = RelatedPanchayat.objects.create(
        name="Bhiti Rawot",
        category="SAHJANWA_GP",
        tehsil="Sahjanwa",
        district="Gorakhpur",
        state="Uttar Pradesh",
        distance_km=3.5,
        notes="Gram Panchayat in Sahjanwa Block"
    )
    assert rel.get_category_display() == "Other Sahjanwa-area Gram Panchayats"

@pytest.mark.django_db
def test_about_village_view(client, village):
    url = reverse('village:about')
    response = client.get(url)
    assert response.status_code == 200
    assert b"Tenuhari (Shukla)" in response.content
    assert b"MOHANLAL" in response.content

@pytest.mark.django_db
def test_condition_dashboard_view(client, village):
    url = reverse('village:conditions')
    response = client.get(url)
    assert response.status_code == 200
    assert b"Tenuhari Village Condition Overview" in response.content
