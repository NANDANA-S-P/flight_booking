from django.shortcuts import render
from flights. models import Airline,Airport,Flight,Seat,SeatType
import sweetify
from datetime import datetime
# Create your views here.
def dashboard(request):
    return render(request,"dashboard/main.html")

def airports(request):
    airports=Airport.objects.all()
    if request.method=="POST":
        code=request.POST["code"]
        location=request.POST["location"]
        Airport.objects.create(code=code,location=location,added_by=request.user)
        sweetify.success(request,"Airport added successfully!",button="OK")
    return render(request,"dashboard/airports.html",{"is_airports_active":True,"airports":airports})

def airlines(request):
    airlines=Airline.objects.all()
    if request.method=="POST":
        name=request.POST["name"]
        logo=request.FILES["logo"]
        Airline.objects.create(name=name,logo=logo,added_by=request.user)
        sweetify.success(request,"Airline added!",button="OK")
   
    return render(request,"dashboard/airlines.html",{'airlines':airlines,'is_airlines_active':True})

def dashboard_flights(request):
    places=Airport.objects.all()
    airlines=Airline.objects.all()
    if request.method=="POST":
        plane_number=request.POST["plane_number"]
        airline_id=request.POST["airlines"]
        source_id=request.POST["source"]
        destination_id=request.POST["destination"]
        departure=request.POST["departure"]
        arrival=request.POST["arrival"]
        business_class_fare=request.POST["business"]
        economy_class_fare=request.POST["economy"]
        first_class_fare=request.POST["first"]

        airline=Airline.objects.get(id=airline_id)
        source=Airport.objects.get(id=source_id)
        destination=Airport.objects.get(id=destination_id)
        is_booking_open=False
        if 'bookings_open' in request.POST:
            is_booking_open = True
       

        flight_obj=Flight.objects.create(plane_number=plane_number,airlines=airline,source=source,destination=destination,departure=departure,arrival=arrival,is_booking_open=is_booking_open,added_by=request.user)
        first_class_type=SeatType.objects.create(flight=flight_obj,type=SeatType.FIRST,fare=first_class_fare)
        business_class_type=SeatType.objects.create(flight=flight_obj,type=SeatType.BUSINESS,fare=business_class_fare)
        economy_class_type=SeatType.objects.create(flight=flight_obj,type=SeatType.ECONOMY,fare=economy_class_fare)
        for i in range(1,11):
            seat_code=plane_number+"-"+str(i)
            Seat.objects.create(code=seat_code,type=first_class_type)
        for i in range(11,36):
            seat_code=plane_number+"-"+str(i)
            Seat.objects.create(code=seat_code,type=business_class_type)
        for i in range(36,61):
            seat_code=plane_number+"-"+str(i)
            Seat.objects.create(code=seat_code,type=economy_class_type)

    return render(request,"dashboard/dashboard_flights.html",{"places":places,"airlines":airlines,"is_flights_active":True})
