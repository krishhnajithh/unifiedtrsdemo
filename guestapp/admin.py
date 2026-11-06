from django.contrib import admin
from .models import Restaurant, Table, TableBooking

admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(TableBooking)
