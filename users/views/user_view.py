from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Profile
from ..forms import ProfileForm


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
