from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.utils.encoding import smart_str, uri_to_iri
from django.urls import reverse
from django.utils import timezone
import os, datetime

from .models import Assignment, AssignmentFile, RenderedFiles, File
from .forms import DocumentForm

@login_required
def list_assignments(request):
    not_before = timezone.now() - datetime.timedelta(days=7)
    list = Assignment.objects.filter(end_at__gte=not_before).order_by('start_at')
    return render(request, 'exams/list_assignments.html', { 'list': list })

@login_required
def list_files(request):
    list = RenderedFiles.objects.filter(user=request.user).order_by('uploaded_at')
    return render(request, 'exams/list_files.html', { 'list': list })

@login_required
def form_upload(request,assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    # die if trying to upload finished or unstarted assignment
    if not assignment.current(): return redirect('home')
    # on form post
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            rendered_instance = form.save(commit=False)
            rendered_instance.assignment = assignment
            rendered_instance.user = request.user
            rendered_instance.save()
            for f in request.FILES.getlist('files'):
                file = File(file=f, rendered=rendered_instance)
                file.save()
            messages.success(request, 'Documents envoyés !')
            return redirect('home')
        else:
            messages.error(request, 'Erreur en envoyant les documents.')
    else:
        form = DocumentForm()
    return render(request, 'exams/form_upload.html', { 'form': form, 'assignment': assignment })

# download view for rendered files
@login_required
def download(request, rendered_id=None, **kwargs):
    # select file object
    rendered = get_object_or_404(RenderedFiles, id=rendered_id)
    # check if user correspons to file or is staff
    if rendered.user == request.user or request.user.is_staff:
        filepath = os.path.join(settings.MEDIA_ROOT, request.path.lstrip('/'))
        return FileResponse(open(filepath, 'rb'), as_attachment=True)
    # otherwise returns error
    else:
        messages.error(request, "Impossible d'accéder à ce fichier.")
        return redirect('home')

# download view for assignment files
@login_required
def assignment(request, assignment_id=None, **kwargs):
    # select corresponding assignment
    assignment = get_object_or_404(Assignment, id=assignment_id)
    # check if the assignment is current or user is staff
    if assignment.current() or request.user.is_staff:
        filepath = os.path.join(settings.MEDIA_ROOT, request.path.lstrip('/'))
        return FileResponse(open(filepath, 'rb'), as_attachment=False)
    # otherwise returns error
    else:
        messages.error(request, "Impossible d'accéder à ce fichier.")
        return redirect('home')
