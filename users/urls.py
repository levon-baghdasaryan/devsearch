from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.index, name='index'),
    path('users/<str:id>/', views.show, name='show'),
    path('account/', views.account, name='account'),
    path('edit/', views.edit, name='edit'),

    path('create-skill/', views.create_skill, name='create-skill'),
    path('edit-skill/<str:id>/', views.edit_skill, name='edit-skill'),
    path('delete-skill/<str:id>/', views.delete_skill, name='delete-skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:id>/', views.view_message, name='message'),
    path('create-message/<str:id>/', views.create_message,
         name='create-message'),
]
