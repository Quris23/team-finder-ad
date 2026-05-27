import json

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EditProfileForm, LoginForm, RegistrationForm
from .models import Skill, User


def register_view(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('projects:list')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('projects:list')


def user_detail_view(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/user-details.html', {'user': profile_user})


@login_required
def edit_profile_view(request):
    form = EditProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('users:detail', user_id=request.user.pk)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('users:detail', user_id=request.user.pk)
    return render(request, 'users/change_password.html', {'form': form})


def users_list_view(request):
    skill_name = request.GET.get('skill', '').strip()
    qs = User.objects.filter(is_active=True)
    if skill_name:
        qs = qs.filter(skills__name=skill_name)
    all_skills = Skill.objects.all()
    paginator = Paginator(qs, 12)
    participants = paginator.get_page(request.GET.get('page'))
    return render(request, 'users/participants.html', {
        'participants': participants,
        'all_skills': all_skills,
        'active_skill': skill_name,
    })


def skills_search_view(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse([], safe=False)
    results = Skill.objects.filter(name__icontains=q)[:10]
    return JsonResponse([{'id': s.id, 'name': s.name} for s in results], safe=False)


@login_required
def add_skill_view(request, user_id):
    if request.user.pk != user_id:
        return JsonResponse({'error': 'Нет доступа'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректный запрос'}, status=400)

    skill_id = data.get('skill_id')
    name = data.get('name', '').strip()

    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif name:
        skill, _ = Skill.objects.get_or_create(name=name)
    else:
        return JsonResponse({'error': 'Не указан навык'}, status=400)

    request.user.skills.add(skill)
    return JsonResponse({'id': skill.id, 'name': skill.name})


@login_required
def remove_skill_view(request, user_id, skill_id):
    if request.user.pk != user_id:
        return JsonResponse({'error': 'Нет доступа'}, status=403)
    skill = get_object_or_404(Skill, pk=skill_id)
    request.user.skills.remove(skill)
    return JsonResponse({'status': 'ok'})
