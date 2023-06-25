from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Airport(models.Model):
    code=models.CharField(max_length=20)
    location=models.CharField(max_length=200)
    added_by=models.ForeignKey(User,related_name="added_airports",null=True,on_delete=models.SET_NULL)
    added_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class Airline(models.Model):
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to="airline_logo/")
    added_by=models.ForeignKey(User,related_name="added_airlines",null=True,on_delete=models.SET_NULL)
    added_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Flight(models.Model):
    plane_number=models.CharField(max_length=50)
    airlines=models.ForeignKey(Airline,on_delete=models.CASCADE,related_name="airline_associated_flights")
    source=models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="flights_from_source")
    destination=models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="flights_as_destination")
    departure=models.DateTimeField()
    arrival=models.DateTimeField()
    is_booking_open=models.BooleanField()
    added_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="added_flights")
    added_at=models.DateTimeField(auto_now_add=True)
    fare=models.IntegerField()


    def __str__(self):
        return f"{self.plane_number}-{self.source.code}-{self.destination.code}"

# class SeatType(models.Model):
#     FIRST=1
#     BUSINESS=2
#     ECONOMY=3
#     SEAT_TYPE=((FIRST,"First"),(BUSINESS,"Business"),(ECONOMY,"Economy"))
#     flight=models.ForeignKey(Flight,on_delete=models.CASCADE,related_name="flight_seats")
#     type=models.SmallIntegerField(choices=SEAT_TYPE)
#     fare=models.IntegerField()

#     def __str__(self):
#         return f"{self.type}-{self.flight.plane_number}"

class Seat(models.Model):
    AVAILABLE=0
    BOOKED=1
    STATUS_CHOICES=((AVAILABLE,"Available"),(BOOKED,"Booked"))
    code=models.CharField(max_length=20)
    flight=models.ForeignKey(Flight,on_delete=models.CASCADE,related_name="associated_seats")
    status =models.IntegerField(choices=STATUS_CHOICES,default=0)

    def __str__(self):
        return self.code
    
class Booking(models.Model):
    INITIATED=0
    PAID=1
    STATUS_CHOICES=((INITIATED,"Initiated"),(PAID,"Paid"))
    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="associated_bookings")
    date_time=models.DateTimeField(auto_now_add=True)
    status=models.IntegerField(choices=STATUS_CHOICES)
    flight=models.ForeignKey(Flight,on_delete=models.SET_NULL,null=True,related_name="related_bookings")

    def __str__(self):
        return f"{self.customer.email}-{self.seat_id}"
    
class Passenger(models.Model):
    MALE=1
    FEMALE=2
    OTHERS=3
    GENDER_CHOICES=((MALE,"Male"),(FEMALE,"Female"),(OTHERS,"Others"))
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    gender=models.SmallIntegerField(choices=GENDER_CHOICES)
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE,related_name="associated_passengers")
    seat_id=models.ForeignKey(Seat,on_delete=models.CASCADE,related_name="related_booking")

    def __str__(self):
        return f"{self.first_name}-{self.seat_id}"
