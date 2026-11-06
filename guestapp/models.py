

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from adminapp.models import Service

class OTPVerification(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class TrainBooking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="train_bookings"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="train_bookings"
    )

    travel_date = models.DateField()

    travel_class = models.CharField(max_length=50)

    passengers = models.IntegerField()

    total_price = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.service_name}"
    
class HotelBooking(models.Model):

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="guest_hotel_bookings"
)

    service = models.ForeignKey(
    Service,
    on_delete=models.CASCADE,
    related_name="guest_hotel_bookings"
)

    check_in = models.DateField()
    check_out = models.DateField()

    room_type = models.CharField(max_length=50)

    guests = models.IntegerField()

    total_price = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.service_name}"

class SeatBooking(models.Model):

    user = models.ForeignKey(
       User,
       on_delete=models.CASCADE,
       related_name="guest_seat_bookings"
   )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    seat_number = models.CharField(max_length=10)

    show_date = models.DateField(null=True, blank=True)
    show_time = models.CharField(max_length=20, null=True, blank=True)

    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service} - {self.seat_number}"
    
class BusBooking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bus_bookings"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="bus_bookings"
    )

    travel_date = models.DateField()

    seat_number = models.CharField(max_length=5)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.seat_number}"
    
class Restaurant(models.Model):
    service = models.OneToOneField(
        Service,
        on_delete=models.CASCADE,
        null=True,        # ✅ allow temporary null
        blank=True
    )
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurants/')

    def __str__(self):
        return self.name


class Table(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=True,     # ✅ temporary
        blank=True
    )
    table_number = models.IntegerField()
    seats = models.IntegerField()
    def __str__(self):
        return f"Table {self.table_number} - {self.service.name}"

class TableBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    guests = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.table}"