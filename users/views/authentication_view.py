from django.shortcuts import render, redirect
from django.contrib.auth import (
    login as login_user, logout as logout_user, authenticate, get_user_model
)
from django.contrib import messages

from ..forms import CustomUserCreationForm


def login(request):
    if request.user.is_authenticated:
        return redirect('users:index')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            get_user_model().objects.get(username=username)
        except Exception:
            messages.error(request, 'Username does not exist')
            print('Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login_user(request, user)
            return redirect(request.GET.get('next') or 'users:account')
        else:
            messages.error(request, 'Username OR password is incorrect.')
            print('Username OR password is incorrect.')

    return render(request, 'users/auth/login.html')


def logout(request):
    logout_user(request)
    messages.info(request, 'User logged out!')
    return redirect('users:login')


def register(request):
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
            login_user(request, user)
            return redirect('users:edit')

    context = {'form': form}
    return render(request, 'users/auth/register.html', context)
