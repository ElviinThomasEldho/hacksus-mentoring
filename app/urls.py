from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.loginUser, name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('register/', views.registerUser, name='registerUser'),
    path('register-team/', views.registerTeam, name='registerTeam'),
    path('team/', views.teamDashboard, name='teamDashboard'),

    path('mentor/', views.mentorDashboard, name='mentorDashboard'),
    path('view-ticket/<int:pk>/', views.viewTicket, name='viewTicket'),
    path('accept-ticket/<int:pk>/', views.acceptTicket, name='acceptTicket'),
    path('close-ticket/<int:pk>/', views.closeTicket, name='closeTicket'),
    path('reopen-ticket/<int:pk>/', views.reopenTicket, name='reopenTicket'),
]
