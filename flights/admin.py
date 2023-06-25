from django.contrib import admin

# Register your models here.
from . models import *
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(Airline)
admin.site.register(Airport)
# admin.site.register(SeatType)
admin.site.register(Seat)
admin.site.register(Passenger)


