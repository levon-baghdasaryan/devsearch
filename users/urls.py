from django.urls import path

from .views import auth_view, user_view, skill_view, message_view

app_name = 'users'
urlpatterns = [
    path('login/', auth_view.login, name='login'),
    path('logout/', auth_view.logout, name='logout'),
    path('register/', auth_view.register, name='register'),

    path('', user_view.index, name='index'),
    path('users/account/', user_view.account, name='account'),
    path('users/edit/', user_view.edit, name='edit'),
    path('users/<str:id>/', user_view.show, name='show'),

    path('skills/create/', skill_view.create_skill, name='create-skill'),
    path('skills/edit/<str:id>/', skill_view.edit_skill, name='edit-skill'),
    path('skills/delete/<str:id>/', skill_view.delete_skill,
         name='delete-skill'),

    path('messages/', message_view.index, name='inbox'),
    path('messages/<str:id>/', message_view.show, name='message'),
    path('messages/create/<str:id>/', message_view.create,
         name='create-message'),
]
