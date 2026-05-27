from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm
from .models import Project, STATUS_CLOSED

PROJECTS_PER_PAGE = 12


def paginate_queryset(request, queryset, per_page=PROJECTS_PER_PAGE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get('page'))


def project_list_view(request):
    projects_qs = (
        Project.objects
        .select_related('owner')
        .prefetch_related('participants')
        .order_by('-created_at')
    )
    projects = paginate_queryset(request, projects_qs)
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
        return JsonResponse(
            {'error': 'Method not allowed'},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    project = Project.objects.filter(pk=project_id, owner=request.user).first()
    if project is None:
        return JsonResponse({'error': 'Not found'}, status=HTTPStatus.NOT_FOUND)
    project.status = STATUS_CLOSED
    project.save(update_fields=['status'])
    return JsonResponse({'status': 'ok'})


@login_required
def toggle_participate_view(request, project_id):
    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Method not allowed'},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse({'error': 'Not found'}, status=HTTPStatus.NOT_FOUND)
    if request.user == project.owner:
        return JsonResponse(
            {'error': 'Owner cannot participate'},
            status=HTTPStatus.BAD_REQUEST,
        )
    is_participant = project.participants.filter(id=request.user.id).exists()
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({'status': 'ok', 'participant': not is_participant})
