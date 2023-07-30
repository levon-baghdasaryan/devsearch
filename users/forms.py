from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .models import Profile, Skill


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            # field.help_text = None
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name', 'email', 'username', 'location', 'bio', 'short_intro',
            'profile_image', 'social_github', 'social_twitter',
            'social_linkedin', 'social_youtube', 'social_website'
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            # field.help_text = None
            field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
