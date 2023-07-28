from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages

from .models import Profile
from .forms import CustomUserCreationForm


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
    messages.error(request, 'User logged out!')
    return redirect('users:login')


def registerUser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('users:index')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def index(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
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
