from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProjectFeedback
from apps.development.models import DevelopmentProject

@login_required
def submit_feedback(request, project_id):
    project = get_object_or_404(DevelopmentProject, pk=project_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        photo = request.FILES.get('photo')

        if not rating or not comment:
            messages.error(request, "Please provide both a rating and a comment.")
            return redirect('development:detail', pk=project_id)

        # Check existing submission
        if ProjectFeedback.objects.filter(project=project, user=request.user).exists():
            messages.warning(request, "You have already submitted feedback for this project.")
            return redirect('development:detail', pk=project_id)

        ProjectFeedback.objects.create(
            project=project,
            user=request.user,
            rating=int(rating),
            comment=comment,
            photo=photo
        )
        messages.success(request, "Thank you! Your feedback has been recorded.")
        return redirect('development:detail', pk=project_id)

    return redirect('development:detail', pk=project_id)
