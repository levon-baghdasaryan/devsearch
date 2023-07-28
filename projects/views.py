from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Project
from .forms import ProjectForm


def index(request):
    print('hello')
    projects = Project.objects.all()

    return render(
        request,
        'projects/index.html',
        {'projects': projects}
    )


@login_required(login_url='users:login')
def create(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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


@login_required(login_url='users:login')
def edit(request, id):
    project = Project.objects.get(id=id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:index')

    context = {'form': form}
    return render(request, 'projects/create-edit.html', context)


@login_required(login_url='users:login')
def delete(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect('projects:index')
    context = {'object': project}
    return render(request, 'projects/delete-template.html', context)
