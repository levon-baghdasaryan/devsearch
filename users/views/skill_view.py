from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..forms import SkillForm


@login_required
def create(request):
    form = SkillForm(request.POST or None)
    if form.is_valid():
        skill = form.save(commit=False)
        skill.owner = request.user.profile
        skill.save()
        messages.success(request, 'Skill was added successfully!')
        return redirect('users:account')
    context = {'form': form}
    return render(request, 'users/skills/create.html', context)


@login_required
def edit(request, id):
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
    return render(request, 'users/skills/edit.html', context)


@login_required
def delete(request, id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=id)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was successfully deleted!')
        return redirect('users:account')
    context = {'object': skill}
    return render(request, 'delete-template.html', context)
