from django.urls import path
from . import views # Tady importujeme views, protože jsme ve stejné složce

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.team_list, name='team_list'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
]