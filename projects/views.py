from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Project, Tag
from .forms import ProjectForm, ReviewForm


def index(request):
    search_query = request.GET.get('q', '')
    page_num = request.GET.get('page', 1)
    paginator = Paginator(Project.objects.search(search_query), 3)

    try:
        projects = paginator.page(page_num)
    except PageNotAnInteger:
        page_num = 1
        projects = paginator.page(page_num)
    except EmptyPage:
        page_num = paginator.num_pages
        projects = paginator.page(page_num)

    page_num = int(page_num)
    left_index = page_num - 2

    if left_index < 1:
        left_index = 1

    right_index = page_num + 3

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return render(
        request,
        'projects/index.html',
        {
            'projects': projects,
            'search_query': search_query,
            'custom_range': custom_range,
        }
    )


@login_required
def create(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            messages.success(request, "You successfully added a project.")
            return redirect('users:account')

    context = {'form': form}
    return render(request, 'projects/create-edit.html', context)


def show(request, id):
    project = Project.objects.get(id=id)
    form = ReviewForm(request.POST or None)

    if form.is_valid():
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        project.getVoteCount
        messages.success(request, 'Your review was successfully submitted!')
        form = ReviewForm()

    return render(
        request,
        'projects/show.html',
        {
            'project': project,
            'form': form,
        }
    )


@login_required
def edit(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('users:account')

    context = {
        'form': form,
        'project': project
    }
    return render(request, 'projects/create-edit.html', context)


@login_required
def delete(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    if request.method == 'POST':
        project.delete()
        return redirect('projects:index')
    context = {'object': project}
    return render(request, 'delete-template.html', context)
