from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Profile
from ..forms import MessageForm


@login_required
def index(request):
    profile = request.user.profile
    messageObjs = profile.messages.all()
    unread_count = messageObjs.filter(is_read=False).count()
    context = {
        'messageObjs': messageObjs,
        'unread_count': unread_count,
    }
    return render(request, 'users/messages/index.html', context)


@login_required
def show(request, id):
    profile = request.user.profile
    message = profile.messages.get(id=id)
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/messages/show.html', context)


def create(request, id):
    recipient = Profile.objects.get(id=id)
    sender = None
    if request.user.is_authenticated:
        sender = request.user.profile

    form = MessageForm(request.POST or None)
    if form.is_valid():
        message = form.save(commit=False)
        message.sender = sender
        message.recipient = recipient

        if sender:
            message.name = sender.name
            message.email = sender.email
        message.save()
        messages.success(request, 'Your message was successfully sent!')
        return redirect('users:show', id=recipient.id)

    context = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'users/messages/form.html', context)
