import pytest
from apps.accounts.models import User, UserRole
from apps.village.models import Village
from apps.complaints.models import Complaint, ComplaintCategory, ComplaintPriority, ComplaintStatus

@pytest.mark.django_db
def test_complaint_ticket_creation():
    village = Village.objects.create(name="Tenuhari (Shukla)", gram_panchayat="Tenuhari (Shukla) Gram Panchayat", block="Sahjanwa", district="Gorakhpur", state="Uttar Pradesh", pincode="273209")
    user = User.objects.create_user(username="villager_cmp", password="password123", role=UserRole.VILLAGER)
    cat = ComplaintCategory.objects.create(name="Water Leakage", description="Desc")

    cmp_obj = Complaint.objects.create(
        ticket_number="CMP-2026-9999",
        user=user,
        category=cat,
        title="Broken Handpump",
        description="Handpump leaking water near street corner",
        location="Near Temple",
        village=village,
        priority=ComplaintPriority.HIGH,
        status=ComplaintStatus.SUBMITTED
    )

    assert cmp_obj.ticket_number == "CMP-2026-9999"
    assert cmp_obj.status == ComplaintStatus.SUBMITTED
