from multiprocessing import context

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Service
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib import messages
from guestapp.models import SeatBooking, TrainBooking, BusBooking, HotelBooking
from django.contrib.admin.views.decorators import staff_member_required
# =========================
# ADMIN LOGIN
# =========================
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'admin/admin_login.html', {
                'error': 'Invalid username or password'
            })

        if not user.is_staff:
            return render(request, 'admin/admin_login.html', {
                'error': 'You are not authorized as admin'
            })

        login(request, user)
        return redirect('adminapp:admin_dashboard')

    return render(request, 'admin/admin_login.html')


@login_required(login_url='adminapp:admin_login')
def admin_dashboard(request):
    total_users = User.objects.filter(is_staff=False).count()
    recent_users = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]

    return render(request, 'admin/admin_dashboard.html', {
        'total_users': total_users,
        'recent_users': recent_users
    })


def admin_logout(request):
    logout(request)
    return redirect('adminapp:admin_login')
# =========================
# ADMIN USERS
# =========================
def admin_users(request):

    query = request.GET.get('q')
    users = User.objects.filter(is_staff=False)

    if query:
        users = users.filter(username__icontains=query)

    return render(request, 'admin/admin_users.html', {
        'users': users,
        'query': query
    })


def delete_user(request, user_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('adminapp:admin_login')

    user = get_object_or_404(User, id=user_id)

    if user.is_staff:
        return redirect('adminapp:admin_users')

    if request.method == 'POST':
        user.delete()

    return redirect('adminapp:admin_users')


# =========================
# ADMIN SERVICES
# =========================
def admin_services(request):

    services = Service.objects.all()

    service_type = request.GET.get("type")

    if service_type:
        services = services.filter(code=service_type)

    return render(request, "admin/admin_services.html", {
        "services": services
    })


# ADD SERVICE
def add_service(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        location = request.POST.get("location")

        if not name or not code or not description or not image:
            messages.error(request, "All required fields must be filled.")
            return redirect("adminapp:add_service")

        Service.objects.create(
            name=name,
            code=code,
            description=description,
            image=image,
            is_active=True,

            # Travel services
            source=source if code in ["train", "bus"] else None,
            destination=destination if code in ["train", "bus"] else None,

            # Location based services (INCLUDING MOVIE)
            location=location if code in ["hotel", "restaurant", "movie"] else None,
        )

        messages.success(request, "Service added successfully!")
        return redirect("adminapp:admin_services")

    return render(request, "admin/service_form.html")


# DELETE SERVICE
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, "Service deleted successfully.")
    return redirect("adminapp:admin_services")

@login_required
def toggle_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.is_active = not service.is_active
    service.save()
    return redirect('adminapp:admin_services')

@staff_member_required
def admin_bookings(request):

    movie_bookings = SeatBooking.objects.select_related("user", "service").all().order_by("-booking_date")

    train_bookings = TrainBooking.objects.select_related("user", "service").all().order_by("-created_at")

    bus_bookings = BusBooking.objects.select_related("user", "service").all().order_by("-created_at")

    hotel_bookings = HotelBooking.objects.select_related("user", "service").all().order_by("-created_at")

    context = {
        "movie_bookings": movie_bookings,
        "train_bookings": train_bookings,
        "bus_bookings": bus_bookings,
        "hotel_bookings": hotel_bookings
    }

    return render(request, "admin/admin_bookings.html", context)