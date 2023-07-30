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
]
