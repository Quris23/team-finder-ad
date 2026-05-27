import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm
from .models import Project


def project_list_view(request):
    projects_qs = (
        Project.objects
        .select_related('owner')
        .prefetch_related('participants')
        .order_by('-created_at')
    )
    paginator = Paginator(projects_qs, 12)
    projects = paginator.get_page(request.GET.get('page'))
    return render(request, 'projects/project_list.html', {'projects': projects})


def project_detail_view(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('participants'),
        pk=project_id,
    )
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('projects:detail', project_id=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:detail', project_id=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


@login_required
def complete_project_view(request, project_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    project = get_object_or_404(Project, pk=project_id, owner=request.user)
    project.status = 'closed'
    project.save(update_fields=['status'])
    return JsonResponse({'status': 'ok'})


@login_required
def toggle_participate_view(request, project_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    project = get_object_or_404(Project, pk=project_id)
    if request.user == project.owner:
        return JsonResponse({'error': 'Owner cannot participate'}, status=400)
    if request.user in project.participants.all():
        project.participants.remove(request.user)
        is_participant = False
    else:
        project.participants.add(request.user)
        is_participant = True
    return JsonResponse({'status': 'ok', 'participant': is_participant})
