from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Project
from .forms import ProjectForm


def index(request):
    projects = Project.objects.all()

    return render(
        request,
        'projects/index.html',
        {'projects': projects}
    )


@login_required
def create(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, "You successfully added a project.")
            return redirect('projects:index')

    context = {'form': form}
    return render(request, 'projects/create-edit.html', context)


def show(request, id):
    project = Project.objects.get(id=id)

    return render(
        request,
        'projects/show.html',
        {'project': project}
    )


@login_required
def edit(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:index')

    context = {'form': form}
    return render(request, 'projects/create-edit.html', context)


@login_required
def delete(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect('projects:index')
    context = {'object': project}
    return render(request, 'projects/delete-template.html', context)
