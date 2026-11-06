from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_users, name='admin_users'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path("services/", views.admin_services, name="admin_services"),
    path("services/add/", views.add_service, name="add_service"),
    path("services/delete/<int:service_id>/", views.delete_service, name="delete_service"),
    path('services/toggle/<int:service_id>/', views.toggle_service, name='toggle_service'),
    path("bookings/", views.admin_bookings, name="admin_bookings"),
]
