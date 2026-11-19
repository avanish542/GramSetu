import pytest
from apps.village.models import Village
from apps.development.models import DevelopmentProject, ProjectCategory, ProjectStatus

@pytest.mark.django_db
def test_project_budget_calculations():
    village = Village.objects.create(name="Tenuhari (Shukla)", gram_panchayat="Tenuhari (Shukla) Gram Panchayat", block="Sahjanwa", district="Gorakhpur", state="Uttar Pradesh", pincode="273209")
    cat = ProjectCategory.objects.create(name="Roads", slug="roads", description="Desc")

    proj = DevelopmentProject.objects.create(
        project_id="PRJ-TEST-0001",
        name="Test CC Road",
        category=cat,
        description="Desc",
        location="Loc",
        village=village,
        estimated_cost=1000000,
        approved_budget=1000000,
        amount_spent=600000,
        funding_source="15th FC",
        status=ProjectStatus.IN_PROGRESS,
        progress_percentage=60
    )

    assert proj.remaining_budget == 400000
