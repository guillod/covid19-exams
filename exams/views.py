from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages

from .models import RenderedFiles, File, Assignment
from .forms import DocumentForm

def home(request):
    documents = RenderedFiles.objects.all()
    return render(request, 'exams/home.html', { 'documents': documents })

def form_upload(request,assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    # die if trying to upload finished  or unstarted assignment
    if not assignment.current(): return redirect('home')
    # on form post
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            rendered_instance = form.save(commit=False)
            rendered_instance.assignment = assignment
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
    return render(request, 'exams/form_upload.html', { 'form': form })

def list_assignments(request):
    list = Assignment.objects.order_by('start_at')
    return render(request, 'exams/list_assignments.html', { 'list': list })
