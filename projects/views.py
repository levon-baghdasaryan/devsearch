from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
import os


def index(request):
    projects = Project.objects.all()

    return render(
        request,
        'projects/index.html',
        {'projects': projects}
    )

def create(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'projects/create-edit.html', context)

def show(request, id):
    project = Project.objects.get(id=id)

    return render(
        request,
        'projects/show.html',
        {'project': project}
    )

def edit(request, id):
    project = Project.objects.get(id=id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'projects/create-edit.html', context)

def delete(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect('home')
    context = {'object': project}
    return render(request, 'projects/delete-template.html', context)