from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=""),
    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login_user, name='guest_login'),
    path('login-otp/', views.verify_login_otp, name='login_otp'),
    path("services/", views.services_home, name="guest_services"),
    path("services/category/<str:code>/", views.services_by_category, name="services_by_category"),
    path("book/<int:service_id>/", views.book_service, name="book_service"),
    path("services/<int:service_id>/", views.service_detail, name="service_detail"),
    path('select-show/<int:service_id>/', views.select_show, name='select_show'),
    path('select-seats/<int:service_id>/', views.select_seats, name='select_seats'),
    path("hotel-booking/<int:service_id>/", views.hotel_booking, name="hotel_booking"),
    path("train-booking/<int:service_id>/", views.train_booking, name="train_booking"),
    path("bus-booking/<int:service_id>/", views.bus_booking, name="bus_booking"),
    path("payment/", views.payment_page, name="payment_page"),
    path("complete-booking/", views.complete_booking, name="complete_booking"),
    path("restaurant-booking", views.restaurant_step1, name="restaurant_step1"),
    path("restaurant-tables/", views.restaurant_tables, name="restaurant_tables"),
    path("booking-success/", views.booking_success, name="booking_success"),
    path("booking-history/", views.booking_history, name="booking_history"),
]