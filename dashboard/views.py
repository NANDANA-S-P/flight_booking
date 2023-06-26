from django.shortcuts import render, redirect
from flights. models import Airline,Airport,Flight,Seat,Booking,Passenger
from django.contrib.auth.decorators import login_required

import sweetify
from datetime import datetime
# Create your views here.
# @login_required
# def dashboard(request):
#     return render(request,"dashboard/main.html")

@login_required
def airports(request):
    if not request.user.profile.is_admin:
        sweetify.warning(request,"Invalid access",button="OK")
        return redirect("flights")
    airports=Airport.objects.all()
    if request.method=="POST":
        code=request.POST["code"]
        location=request.POST["location"]
        Airport.objects.create(code=code,location=location,added_by=request.user)
        sweetify.success(request,"Airport added successfully!",button="OK")
    return render(request,"dashboard/airports.html",{"is_airports_active":True,"airports":airports})

@login_required
def airlines(request):
    if not request.user.profile.is_admin:
        sweetify.warning(request,"Invalid access",button="OK")
        return redirect("flights")
    airlines=Airline.objects.all()
    if request.method=="POST":
        name=request.POST["name"]
        logo=request.FILES["logo"]
        Airline.objects.create(name=name,logo=logo,added_by=request.user)
        sweetify.success(request,"Airline added!",button="OK")
   
    return render(request,"dashboard/airlines.html",{'airlines':airlines,'is_airlines_active':True})

@login_required
def dashboard_flights(request):
    
    if not request.user.profile.is_admin:
        sweetify.warning(request,"Invalid access",button="OK")
        return redirect("flights")
    places=Airport.objects.all()
    airlines=Airline.objects.all()
    flights=Flight.objects.all()
    if request.method=="POST":
        plane_number=request.POST["plane_number"]
        airline_id=request.POST["airlines"]
        source_id=request.POST["source"]
        destination_id=request.POST["destination"]
        departure=request.POST["departure"]
        arrival=request.POST["arrival"]
        fare=request.POST["fare"]
        airline=Airline.objects.get(id=airline_id)
        source=Airport.objects.get(id=source_id)
        destination=Airport.objects.get(id=destination_id)
        is_booking_open=False
        if 'bookings_open' in request.POST:
            is_booking_open = True
       

        flight_obj=Flight.objects.create(plane_number=plane_number,airlines=airline,source=source,destination=destination,departure=departure,arrival=arrival,is_booking_open=is_booking_open,added_by=request.user,fare=fare)
        for i in range(1,61):
            seat_code=plane_number+"-"+str(i)
            Seat.objects.create(code=seat_code,flight=flight_obj)
        sweetify.success(request,"Flight added!",button="OK")
       
    return render(request,"dashboard/dashboard_flights.html",{"places":places,"airlines":airlines,"is_flights_active":True,"flights":flights})


@login_required
def bookings(request):
    if not request.user.profile.is_admin:
        sweetify.warning(request,"Invalid access",button="OK")
        return redirect("flights")
    flights=Flight.objects.all()
    return render(request,"dashboard/bookings.html",{"is_bookings_active":True,"flights":flights})

@login_required
def booking_detail(request,flight_id):
    if not request.user.profile.is_admin:
        sweetify.warning(request,"Invalid access",button="OK")
        return redirect("flights")
    flight_obj=Flight.objects.get(id=flight_id)
    bookings=Booking.objects.filter(flight=flight_obj)
    return render(request,"dashboard/booking_detail.html",{"is_bookings_active":True,"bookings":bookings})

@login_required
def passenger_details(request,booking_id):
    if not request.user.profile.is_admin:
        sweetify.warning(request,"Invalid access",button="OK")
        return redirect("flights")
    booking_obj=Booking.objects.get(id=booking_id)
    passengers=Passenger.objects.filter(booking=booking_obj)
    return render(request,"dashboard/passenger_details.html",{"is_bookings_active":True,"passengers":passengers})