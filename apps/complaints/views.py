import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Complaint, ComplaintStatus, ComplaintUpdate
from .forms import ComplaintSubmissionForm
from apps.village.models import Village

@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            
            village = Village.objects.first()
            complaint.village = village
            
            # Generate CMP-YYYY-XXXX ticket number
            year = timezone.now().year
            count = Complaint.objects.count() + 1
            complaint.ticket_number = f"CMP-{year}-{count:04d}"
            complaint.save()

            # Add initial public update
            ComplaintUpdate.objects.create(
                complaint=complaint,
                status=ComplaintStatus.SUBMITTED,
                note="Complaint registered successfully.",
                updated_by=request.user,
                is_public=True
            )

            messages.success(request, f"Complaint submitted successfully! Your Ticket ID is {complaint.ticket_number}")
            return redirect('complaints:detail', pk=complaint.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ComplaintSubmissionForm()

    return render(request, 'complaints/submit.html', {'form': form})


@login_required
def my_complaints(request):
    """
    List complaints submitted by the authenticated user.
    If Panchayat Admin or Super Admin, show all complaints.
    """
    if request.user.is_panchayat_admin:
        complaint_qs = Complaint.objects.select_related('user', 'category', 'ward').all()
    else:
        complaint_qs = Complaint.objects.select_related('category', 'ward').filter(user=request.user)

    search_query = request.GET.get('q')
    status_filter = request.GET.get('status')

    if search_query:
        complaint_qs = complaint_qs.filter(ticket_number__icontains=search_query) | complaint_qs.filter(title__icontains=search_query)
    if status_filter:
        complaint_qs = complaint_qs.filter(status=status_filter)

    paginator = Paginator(complaint_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'complaints': page_obj,
        'status_choices': ComplaintStatus.choices,
        'selected_status': status_filter,
        'search_query': search_query,
    }
    return render(request, 'complaints/my_complaints.html', context)


@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint.objects.select_related('user', 'category', 'ward', 'assigned_to'), pk=pk)

    # Object-level authorization check: Villager can ONLY access their own complaints
    if not (request.user.is_panchayat_admin or complaint.user == request.user):
        messages.error(request, "You are not authorized to view this complaint ticket.")
        return redirect('complaints:my_complaints')

    updates = complaint.updates.all()
    if not request.user.is_panchayat_admin:
        updates = updates.filter(is_public=True)

    context = {
        'complaint': complaint,
        'updates': updates,
    }
    return render(request, 'complaints/detail.html', context)
