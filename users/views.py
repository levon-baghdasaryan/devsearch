from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('users:index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            get_user_model().objects.get(username=username)
        except Exception:
            messages.error(request, 'Username does not exist')
            print('Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('users:index')
        else:
            messages.error(request, 'Username OR password is incorrect.')
            print('Username OR password is incorrect.')

    return render(request, 'users/login.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User logged out!')
    return redirect('users:login')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('users:index')

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('users:edit')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def index(request):
    search_query = request.GET.get('q', '')
    profiles = Profile.objects.search(search_query)
    context = {
        'profiles': profiles,
        'search_query': search_query,
    }
    return render(request, 'users/index.html', context)


def show(request, id):
    profile = Profile.objects.get(id=id)
    topSkills = profile.skill_set.exclude(description__exact='')
    otherSkills = profile.skill_set.filter(description='')
    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills,
    }
    return render(request, 'users/show.html', context)


@login_required
def edit(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:account')

    context = {'form': form}
    return render(request, 'users/edit.html', context)


@login_required
def account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }
    return render(request, 'users/account.html', context)


@login_required
def create_skill(request):
    form = SkillForm(request.POST or None)
    if form.is_valid():
        skill = form.save(commit=False)
        skill.owner = request.user.profile
        skill.save()
        messages.success(request, 'Skill was added successfully!')
        return redirect('users:account')
    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required
def edit_skill(request, id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=id)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('users:account')
    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


def delete_skill(request, id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=id)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was successfully deleted!')
        return redirect('users:account')
    context = {'object': skill}
    return render(request, 'delete-template.html', context)
