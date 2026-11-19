import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.accounts.models import User, UserRole
from apps.village.models import Village
from apps.services.models import PanchayatService
from apps.applications.models import ServiceApplication, ApplicationDocument, ApplicationStatus

@pytest.mark.django_db
def test_private_document_access_isolation(client):
    village = Village.objects.create(name="TestVillage", gram_panchayat="GP", block="B", district="D", state="S", pincode="110001")
    service = PanchayatService.objects.create(name="Test Cert", slug="test-cert", category="Cat", description="Desc", eligibility="Elig", required_documents="Doc")

    user_a = User.objects.create_user(username="user_a", password="password123", role=UserRole.VILLAGER, village=village)
    user_b = User.objects.create_user(username="user_b", password="password123", role=UserRole.VILLAGER, village=village)

    app_a = ServiceApplication.objects.create(
        application_number="APP-TEST-0001",
        applicant=user_a,
        service=service,
        village=village,
        applicant_name="User A",
        applicant_phone="999",
        applicant_address="Address",
        status=ApplicationStatus.SUBMITTED
    )

    test_file = SimpleUploadedFile("secret_aadhaar.pdf", b"Sensitive Data Content", content_type="application/pdf")
    doc_a = ApplicationDocument.objects.create(
        application=app_a,
        document_name="Secret Aadhaar Card",
        file=test_file,
        mime_type="application/pdf",
        file_size=len(b"Sensitive Data Content")
    )

    # 1. User B tries to view Application A detail page -> Must be rejected / redirected
    client.login(username="user_b", password="password123")
    res_detail = client.get(reverse('applications:detail', kwargs={'pk': app_a.pk}))
    assert res_detail.status_code == 302 # Redirected due to unauthorized access check

    # 2. User B tries to download User A's document -> Must return 404 access denied
    res_doc = client.get(reverse('applications:download_document', kwargs={'doc_id': doc_a.pk}))
    assert res_doc.status_code == 404

    # 3. User A downloads own document -> Must succeed
    client.login(username="user_a", password="password123")
    res_own_doc = client.get(reverse('applications:download_document', kwargs={'doc_id': doc_a.pk}))
    assert res_own_doc.status_code == 200
