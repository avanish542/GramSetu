from rest_framework import serializers
from apps.accounts.models import User
from apps.village.models import Village, Ward
from apps.development.models import DevelopmentProject, ProjectCategory, ProjectImage
from apps.complaints.models import Complaint, ComplaintCategory, ComplaintUpdate
from apps.services.models import PanchayatService
from apps.applications.models import ServiceApplication, ApplicationDocument
from apps.schemes.models import GovernmentScheme
from apps.notices.models import Notice
from apps.gallery.models import GalleryItem
from apps.infrastructure.models import InfrastructureItem

class UserSerializer(serializers.ModelModelSerializer if hasattr(serializers, 'ModelModelSerializer') else serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_verified')
        read_only_fields = ('id', 'is_verified')


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = '__all__'


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'


class DevelopmentProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = DevelopmentProject
        fields = '__all__'


class ComplaintCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintCategory
        fields = '__all__'


class ComplaintUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintUpdate
        fields = '__all__'


class ComplaintSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    updates = ComplaintUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Complaint
        fields = '__all__'
        read_only_fields = ('ticket_number', 'user', 'internal_notes')


class PanchayatServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanchayatService
        fields = '__all__'


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = ('id', 'document_name', 'mime_type', 'file_size', 'created_at')


class ServiceApplicationSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    documents = ApplicationDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceApplication
        fields = '__all__'
        read_only_fields = ('application_number', 'applicant', 'status')


class GovernmentSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentScheme
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = '__all__'


class InfrastructureItemSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = InfrastructureItem
        fields = '__all__'
