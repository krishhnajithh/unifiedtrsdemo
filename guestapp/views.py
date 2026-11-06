import random
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from adminapp.models import Service
from .models import OTPVerification, SeatBooking, TrainBooking, HotelBooking, BusBooking, Restaurant, Table, TableBooking
from datetime import date, time, timedelta
from datetime import date , datetime


# ==========================================
# HOME
# ==========================================
def index(request):
    return render(request, "guest/home.html")


# ==========================================
# REGISTER
# ==========================================
def register(request):

    if request.method == "POST":

        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request,"guest/register.html",{"error":"Username already exists."})

        if User.objects.filter(email=email).exists():
            return render(request,"guest/register.html",{"error":"Email already registered."})

        otp = str(random.randint(100000,999999))

        OTPVerification.objects.update_or_create(
            email=email,
            defaults={"otp":otp}
        )

        request.session["registration_data"]={
            "email":email,
            "username":username,
            "password":password
        }

        send_mail(
            "UTRS OTP Verification",
            f"Your OTP is {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )

        return redirect("verify_otp")

    return render(request,"guest/register.html")


# ==========================================
# VERIFY OTP
# ==========================================
def verify_otp(request):

    data=request.session.get("registration_data")

    if not data:
        return redirect("register")

    if request.method=="POST":

        entered=request.POST.get("otp")

        record=OTPVerification.objects.filter(
            email=data["email"],
            otp=entered
        ).first()

        if record:

            User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"]
            )

            record.delete()
            request.session.pop("registration_data",None)

            return redirect("register_success")

        messages.error(request,"Invalid OTP")

    return render(request,"guest/verify_otp.html")


# ==========================================
# REGISTER SUCCESS
# ==========================================
def register_success(request):
    return render(request,"guest/register_success.html")


# ==========================================
# LOGIN
# ==========================================
def login_user(request):

    if request.method=="POST":

        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)

        if user is None:
            return render(request,"guest/login.html",{"error":"Invalid credentials"})

        otp=str(random.randint(100000,999999))

        OTPVerification.objects.update_or_create(
            email=user.email,
            defaults={"otp":otp}
        )

        request.session["login_email"]=user.email

        send_mail(
            "UTRS Login OTP",
            f"Your login OTP is {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )

        return redirect("login_otp")

    return render(request,"guest/login.html")


# ==========================================
# VERIFY LOGIN OTP
# ==========================================
def verify_login_otp(request):

    email=request.session.get("login_email")

    if not email:
        return redirect("guest_login")

    if request.method=="POST":

        entered=request.POST.get("otp")

        record=OTPVerification.objects.filter(email=email).first()

        if record and record.otp==entered:

            user=User.objects.get(email=email)
            login(request,user)

            record.delete()
            request.session.pop("login_email",None)

            return redirect("guest_services")

        return render(request,"guest/login_otp.html",{"error":"Invalid OTP"})

    return render(request,"guest/login_otp.html")


# ==========================================
# SERVICES HOME
# ==========================================
@login_required(login_url='guest_login')
def services_home(request):
    return render(request,"guest/services_home.html")


# ==========================================
# CATEGORY PAGE
# ==========================================
@login_required(login_url='guest_login')
def services_by_category(request,code):

    services=Service.objects.filter(code=code,is_active=True)

    context={
        "services":services,
        "code":code
    }

    return render(request,"guest/services_by_category.html",context)


# ==========================================
# SERVICE DETAIL
# ==========================================
@login_required(login_url='guest_login')
def service_detail(request,service_id):

    service=get_object_or_404(Service,id=service_id,is_active=True)

    return render(request,"guest/service_detail.html",{"service":service})


# ==========================================
# BOOK SERVICE ROUTER
# ==========================================
@login_required(login_url='guest_login')
def book_service(request,service_id):

    service=get_object_or_404(Service,id=service_id)

    if service.code=="movie":
        return redirect("select_show",service_id=service.id)

    elif service.code=="train":
        return redirect("train_booking",service_id=service.id)

    elif service.code=="bus":
        return redirect("bus_booking",service_id=service.id)

    elif service.code=="hotel":
        return redirect("hotel_booking",service_id=service.id)
     
    elif service.code=="restaurant":
        return redirect("restaurant_step1")

    return redirect("guest_services")


# ==========================================
# MOVIE SHOW SELECTION
# ==========================================
@login_required(login_url='guest_login')
def select_show(request, service_id):

    service = get_object_or_404(Service, id=service_id)

    # 🔥 CLEAR OLD WRONG DATA
    request.session.pop("show_date", None)
    request.session.pop("show_time", None)

    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after = today + timedelta(days=2)

    if request.method == "POST":

        raw_date = request.POST.get("show_date")

        # 🔒 FORCE CORRECT FORMAT
        request.session["show_date"] = str(raw_date)  # ensures YYYY-MM-DD
        request.session["show_time"] = request.POST.get("show_time")

        return redirect("select_seats", service_id=service.id)

    return render(request, "guest/select_show.html", {
        "service": service,
        "dates": [
            {"label": "Today", "value": today},
            {"label": "Tomorrow", "value": tomorrow},
            {"label": day_after.strftime("%d %b"), "value": day_after},
        ]
    })
# ==========================================
# SEAT PRICE
# ==========================================
def get_seat_price(seat):

    row=seat[0]

    if row in ["A","B"]:
        return 250
    elif row in ["C","D"]:
        return 180
    return 120


# ==========================================
# MOVIE SEAT SELECTION
# ==========================================
@login_required(login_url='guest_login')
def select_seats(request,service_id):

    service=get_object_or_404(Service,id=service_id)

    show_date=request.session.get("show_date")
    show_time=request.session.get("show_time")

    booked=SeatBooking.objects.filter(
        service=service,
        show_date=show_date,
        show_time=show_time
    ).values_list("seat_number",flat=True)

    if request.method=="POST":

        seats=request.POST.getlist("seats")

        total=0
        for s in seats:
            total+=get_seat_price(s)

        request.session["booking"]={
            "type":"movie",
            "service_id":service.id,
            "service":service.name,
            "show_date":show_date,
            "show_time":show_time,
            "seats":seats,
            "total":total
        }

        return redirect("payment_page")

    return render(request,"guest/seat_selection.html",{
        "service":service,
        "booked_seats":list(booked),
        "show_date":show_date,
        "show_time":show_time
    })


# ==========================================
# TRAIN BOOKING
# ==========================================
@login_required(login_url='guest_login')
def train_booking(request, service_id):

    service = get_object_or_404(Service, id=service_id)

    # ✅ UPDATED STATIONS (ORDER MATTERS)
    stations = [
        "Kollam",
        "Chengannur",
        "Kottayam",
        "Ernakulam",
        "Thrissur",
        "Kozhikode",
        "Kannur",
        "Kasargode",
    ]

    # ==========================================
    # POST REQUEST
    # ==========================================
    if request.method == "POST":

        from_station = request.POST.get("from_station")
        to_station = request.POST.get("to_station")
        travel_date = request.POST.get("travel_date")
        travel_class = request.POST.get("travel_class")
        passengers = request.POST.get("passengers")

        # ==========================
        # VALIDATIONS
        # ==========================

        # 1. Empty check
        if not from_station or not to_station:
            return render(request, "guest/train_booking.html", {
                "service": service,
                "stations": stations,
                "today": date.today(),
                "error": "Please select both source and destination"
            })

        # 2. Same station
        if from_station == to_station:
            return render(request, "guest/train_booking.html", {
                "service": service,
                "stations": stations,
                "today": date.today(),
                "error": "Source and destination cannot be the same"
            })

        # 3. Station validity
        if from_station not in stations or to_station not in stations:
            return render(request, "guest/train_booking.html", {
                "service": service,
                "stations": stations,
                "today": date.today(),
                "error": "Invalid station selected"
            })

        from_index = stations.index(from_station)
        to_index = stations.index(to_station)

        # 4. Route order check
        if from_index > to_index:
            return render(request, "guest/train_booking.html", {
                "service": service,
                "stations": stations,
                "today": date.today(),
                "error": "Destination must come after source in route"
            })

        # 5. Date validation
        try:
            travel_date_obj = datetime.strptime(travel_date, "%Y-%m-%d").date()
        except:
            return render(request, "guest/train_booking.html", {
                "service": service,
                "stations": stations,
                "today": date.today(),
                "error": "Invalid date format"
            })

        if travel_date_obj < date.today():
            return render(request, "guest/train_booking.html", {
                "service": service,
                "stations": stations,
                "today": date.today(),
                "error": "You cannot book for past dates"
            })

        # 6. Passenger validation
        try:
            passengers = int(passengers)
        except:
            return render(request, "guest/train_booking.html", {
                "service": service,
                "stations": stations,
                "today": date.today(),
                "error": "Invalid number of passengers"
            })

        # ==========================
        # PRICE CALCULATION
        # ==========================

        price = 500
        if travel_class == "AC Chair Car":
            price = 1200
        elif travel_class == "Executive Class":
            price = 2000

        total_price = price * passengers

        # ==========================
        # STORE IN SESSION
        # ==========================

        request.session["booking"] = {
            "type": "train",
            "service_id": service.id,
            "service": service.name,
            "from_station": from_station,
            "to_station": to_station,
            "travel_date": travel_date,
            "travel_class": travel_class,
            "passengers": passengers,
            "total": total_price
        }

        return redirect("payment_page")

    # ==========================================
    # GET REQUEST
    # ==========================================

    return render(request, "guest/train_booking.html", {
        "service": service,
        "stations": stations,
        "today": date.today()
    })
# ==========================================
# HOTEL BOOKING
# ==========================================
@login_required(login_url='guest_login')
def hotel_booking(request,service_id):

    service=get_object_or_404(Service,id=service_id)

    if request.method=="POST":

        check_in=request.POST.get("check_in")
        check_out=request.POST.get("check_out")
        room_type=request.POST.get("room_type")
        guests=request.POST.get("guests")

        price=2000
        if room_type=="Deluxe":
            price=3000
        elif room_type=="Suite":
            price=5000

        request.session["booking"]={
            "type":"hotel",
            "service_id":service.id,
            "service":service.name,
            "check_in":check_in,
            "check_out":check_out,
            "room_type":room_type,
            "guests":guests,
            "total":price
        }

        return redirect("payment_page")

    return render(request,"guest/hotel_booking.html",{"service":service})


# ==========================================
# BUS BOOKING
# ==========================================
@login_required(login_url='guest_login')
def bus_booking(request, service_id):

    service = get_object_or_404(Service, id=service_id)

    # ✅ ONLY GET (not POST)
    travel_date = request.GET.get("travel_date")

    if travel_date:
        booked_seats = BusBooking.objects.filter(
            service=service,
            travel_date=travel_date
        ).values_list('seat_number', flat=True)
    else:
        booked_seats = []

    if request.method == "POST":

        seats = request.POST.getlist("seats")
        travel_date = request.POST.get("travel_date")

        if not seats:
            messages.error(request, "Please select seats")
            return redirect(f"/bus-booking/{service.id}/?travel_date={travel_date}")

        seat_price = 300
        total_price = seat_price * len(seats)

        request.session["booking"] = {
            "type": "bus",
            "service_id": service.id,
            "service": service.name,
            "travel_date": travel_date,
            "seats": seats,
            "total": total_price
        }

        return redirect("payment_page")

    return render(request, "guest/bus_seat_selection.html", {
        "service": service,
        "booked_seats": list(booked_seats),
        "travel_date": travel_date
    })
# ==========================================
# PAYMENT PAGE
# ==========================================
@login_required(login_url='guest_login')
def payment_page(request):

    booking=request.session.get("booking")

    return render(request,"guest/payment.html",{"booking":booking})


# ==========================================
# COMPLETE BOOKING
# ==========================================
@login_required(login_url='guest_login')
def complete_booking(request):

    booking = request.session.get("booking")

    if not booking:
        return redirect("guest_services")

    payment_method = request.POST.get("payment_method")

    service = Service.objects.get(id=booking["service_id"])

    # MOVIE
    if booking["type"] == "movie":

        for seat in booking["seats"]:
            SeatBooking.objects.create(
                user=request.user,
                service=service,
                seat_number=seat,
                show_date=booking["show_date"],
                show_time=booking["show_time"]
            )

    # TRAIN
    elif booking["type"] == "train":

        TrainBooking.objects.create(
            user=request.user,
            service=service,
            travel_date=booking["travel_date"],
            travel_class=booking["travel_class"],
            passengers=booking["passengers"],
            total_price=booking["total"]
        )

    # HOTEL
    elif booking["type"] == "hotel":

        HotelBooking.objects.create(
            user=request.user,
            service=service,
            check_in=booking["check_in"],
            check_out=booking["check_out"],
            room_type=booking["room_type"],
            guests=booking["guests"],
            total_price=booking["total"]
        )

    # BUS
    elif booking["type"] == "bus":

        for seat in booking["seats"]:
            BusBooking.objects.create(
                user=request.user,
                service=service,
                travel_date=booking["travel_date"],
                seat_number=seat
            )

    send_mail(
        "Booking Confirmation",
        f"Your booking for {booking['service']} is confirmed.\nPayment: {payment_method}",
        "ticketreservationsystemunified@gmail.com",
        [request.user.email],
        fail_silently=False
    )

    request.session.pop("booking", None)

    return render(request, "guest/success.html", {"booking": booking})

@login_required
@login_required
def restaurant_step1(request):

    if request.method == "POST":
        guests = request.POST.get("guests")
        time = request.POST.get("time")
        booking_date = request.POST.get("date")  

        if not guests or not time:
            return render(request, "guest/restaurant_step1.html", {
                "error": "Please select time and guests",
                "today": date.today()
            })

        request.session["guests"] = guests
        request.session["booking_time"] = time
        request.session["booking_date"] = str(booking_date)

        return redirect("restaurant_tables")

    return render(request, "guest/restaurant_step1.html", {
        "today": date.today()
    })
@login_required
def restaurant_tables(request):

    tables = Table.objects.all()

    # ✅ Get session data
    guests = request.session.get("guests")
    booking_date = request.session.get("booking_date")
    booking_time = request.session.get("booking_time")

    # ✅ Validate session
    if not guests or not booking_date or not booking_time:
        return redirect("restaurant_step1")

    guests = int(guests)

    # ✅ Get already booked tables (based on date + time)
    booked_tables = TableBooking.objects.filter(
        booking_date=booking_date,
        booking_time=booking_time
    ).values_list('table_id', flat=True)

    # ==========================================
    # POST → CREATE BOOKING + SEND EMAIL
    # ==========================================
    if request.method == "POST":

        table_id = request.POST.get("table")

        if not table_id:
            return render(request, "guest/restaurant_tables.html", {
                "tables": tables,
                "booked_tables": booked_tables,
                "error": "Select a table"
            })

        # ✅ Create booking
        booking = TableBooking.objects.create(
            user=request.user,
            table_id=table_id,
            booking_date=booking_date,
            booking_time=booking_time,
            guests=guests
        )

        # ==========================================
        # 📧 SEND EMAIL
        # ==========================================
        subject = "🍽 Restaurant Booking Confirmed"

        message = f"""
Hi {request.user.username},

Your table booking is confirmed 🎉

📍 Restaurant: {booking.table.service.name}
🍽 Table No: {booking.table.table_number}
📅 Date: {booking.booking_date}
⏰ Time: {booking.booking_time}
👥 Guests: {booking.guests}

We look forward to serving you!

- UTRS Team
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False
        )

        # ✅ Clear session (important)
        request.session.pop("guests", None)
        request.session.pop("booking_date", None)
        request.session.pop("booking_time", None)

        return redirect("booking_success")

    # ==========================================
    # GET → SHOW TABLES
    # ==========================================
    return render(request, "guest/restaurant_tables.html", {
        "tables": tables,
        "booked_tables": booked_tables,
        "guests": guests,
        "booking_date": booking_date,
        "booking_time": booking_time
    })

def booking_success(request):
    return render(request, "guest/booking_success.html")

@login_required
def booking_history(request):

    movie_bookings = SeatBooking.objects.filter(user=request.user)
    bus_bookings = BusBooking.objects.filter(user=request.user)
    train_bookings = TrainBooking.objects.filter(user=request.user)
    hotel_bookings = HotelBooking.objects.filter(user=request.user)
    table_bookings = TableBooking.objects.filter(user=request.user)

    return render(request, "guest/booking_history.html", {
        "movie_bookings": movie_bookings,
        "bus_bookings": bus_bookings,
        "train_bookings": train_bookings,
        "hotel_bookings": hotel_bookings,
        "table_bookings": table_bookings,
    })