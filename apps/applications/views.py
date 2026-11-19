from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import ServiceApplication, ApplicationDocument, ApplicationStatus
from .forms import ApplicationSubmissionForm
from apps.services.models import PanchayatService
from apps.village.models import Village

@login_required
def apply_for_service(request, service_id):
    service = get_object_or_404(PanchayatService, pk=service_id, is_active=True)

    if request.method == 'POST':
        form = ApplicationSubmissionForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.service = service
            application.village = Village.objects.first()

            # Auto-generate APP-YYYY-XXXX number
            year = timezone.now().year
            count = ServiceApplication.objects.count() + 1
            application.application_number = f"APP-{year}-{count:04d}"
            application.status = ApplicationStatus.SUBMITTED
            application.save()

            # Process file uploads
            for file_key in request.FILES:
                uploaded_file = request.FILES[file_key]
                ApplicationDocument.objects.create(
                    application=application,
                    document_name=file_key.replace('_', ' ').title(),
                    file=uploaded_file,
                    mime_type=uploaded_file.content_type or 'application/octet-stream',
                    file_size=uploaded_file.size
                )

            messages.success(
                request,
                f"Application submitted successfully! Your Application ID is {application.application_number}"
            )
            return redirect('applications:detail', pk=application.pk)
        else:
            messages.error(request, "Please fill in all required fields.")
    else:
        initial_data = {
            'applicant_name': request.user.get_full_name() or request.user.username,
            'applicant_phone': request.user.phone or '',
            'ward': request.user.ward,
        }
        form = ApplicationSubmissionForm(initial=initial_data)

    context = {
        'service': service,
        'form': form,
    }
    return render(request, 'applications/apply.html', context)


@login_required
def my_applications(request):
    if request.user.is_panchayat_admin:
        app_qs = ServiceApplication.objects.select_related('applicant', 'service', 'ward').all()
    else:
        app_qs = ServiceApplication.objects.select_related('service', 'ward').filter(applicant=request.user)

    search_query = request.GET.get('q')
    status_filter = request.GET.get('status')

    if search_query:
        app_qs = app_qs.filter(application_number__icontains=search_query) | app_qs.filter(applicant_name__icontains=search_query)
    if status_filter:
        app_qs = app_qs.filter(status=status_filter)

    paginator = Paginator(app_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'applications': page_obj,
        'status_choices': ApplicationStatus.choices,
        'selected_status': status_filter,
        'search_query': search_query,
    }
    return render(request, 'applications/my_applications.html', context)


@login_required
def application_detail(request, pk):
    application = get_object_or_404(
        ServiceApplication.objects.select_related('applicant', 'service', 'ward', 'processed_by')
        .prefetch_related('documents'),
        pk=pk
    )

    # Object-level security authorization check
    if not (request.user.is_panchayat_admin or application.applicant == request.user):
        messages.error(request, "You are not authorized to view this service application.")
        return redirect('applications:my_applications')

    context = {
        'application': application,
        'documents': application.documents.all(),
    }
    return render(request, 'applications/detail.html', context)


@login_required
def download_document(request, doc_id):
    """
    Secure document download endpoint with strict object-level access control.
    Prevents unauthorized access to private villager documents.
    """
    doc = get_object_or_404(ApplicationDocument.objects.select_related('application__applicant'), pk=doc_id)

    # Strict Object-Level Permission Check
    if not (request.user.is_panchayat_admin or doc.application.applicant == request.user):
        raise Http404("Document not found or access denied.")

    if not doc.file or not doc.file.storage.exists(doc.file.name):
        raise Http404("File does not exist.")

    response = HttpResponse(doc.file.read(), content_type=doc.mime_type or 'application/octet-stream')
    response['Content-Disposition'] = f'inline; filename="{doc.document_name}"'
    return response
