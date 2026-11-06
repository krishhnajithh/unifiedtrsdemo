from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Service(models.Model):

    SERVICE_CODES = [
        ('train', 'Train Tickets'),
        ('bus', 'Bus Tickets'),
        ('movie', 'Movie Tickets'),
        ('hotel', 'Hotels'),
        ('restaurant', 'Restaurants'),
    ]

    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, choices=SERVICE_CODES)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    source = models.CharField(max_length=100, blank=True, null=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class HotelRoom(models.Model):

    ROOM_TYPES = [
        ('deluxe','Deluxe'),
        ('super_deluxe','Super Deluxe'),
        ('ac','AC'),
        ('non_ac','Non AC'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=30, choices=ROOM_TYPES)
    room_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.service.name} - {self.room_type} - {self.room_number}"
    
    
# class HotelBooking(models.Model):

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)

#     check_in = models.DateField()
#     check_out = models.DateField()

class HotelBooking(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)

    check_in = models.DateField()
    check_out = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['room','check_in','check_out']
        
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class SeatBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_date = models.DateField()
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.movie.title} - {self.seat_number}"