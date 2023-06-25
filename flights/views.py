from django.shortcuts import render,redirect
from users.models import Profile
from flights.models import Flight, Airport,Seat, Booking,Passenger
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
import sweetify
from django.conf import settings as conf_settings
import stripe

stripe.api_key=conf_settings.STRIPE_SECRET_KEY
# Create your views here.

def flights(request):
    if request.user.is_authenticated:
        profile_obj=Profile.objects.filter(user=request.user)
        if profile_obj:
            flights=Flight.objects.filter(is_booking_open=True)
            airports=Airport.objects.all()
            flight_details=[]

            for flight in flights:
                curr=dict()
                curr['flight_det']=flight
                available_seats=Seat.objects.filter(status=0,flight=flight).count()
                if available_seats>0:
                    curr['seats']=available_seats
                    flight_details.append(curr)


                
            # flight_id=7
            # req_flight_obj=dict()
            # req_flight_obj["source"]="DEL"
            # req_flight_obj["destination"]="CBE"
            # req_flight_obj["seats"]=6
            # print(flight_id)
            # print(seat_class)
            return render(request,"flights/flights.html",{"airports":airports,"flights":flight_details})
        
        else:
            social_auth_obj=UserSocialAuth.objects.filter(uid=request.user.email)
            if social_auth_obj:
                return redirect("details")
            else:
                return redirect("verify")
    else:
        return redirect("login")
    

@login_required
def book(request):
    if request.method=="POST":
        print(request.POST)

        seats=request.POST["f_seats"]
        flight_id=request.POST["flight_id"]
        flight_obj=Flight.objects.get(id=flight_id)
        available_seats=Seat.objects.filter(status=0,flight=flight_obj).count()
        if(int(seats)>available_seats):
            sweetify.warning(request,"Sorry! Requested number of seats is not available")
            return redirect("flights")
        return render(request,"flights/book.html",{"flight_obj":flight_obj,"seats":seats,"fare":(flight_obj.fare)*int(seats),"passengers":range(1,int(seats)+1)})
    


def confirm_booking(request):
    if request.method=="POST":
        seats=request.POST["seats"]
        flight_id=request.POST["flight_id"]
        flight_obj=Flight.objects.get(id=flight_id)
        available_seats=Seat.objects.filter(status=0,flight=flight_obj).count()
        if(int(seats)>available_seats):
            sweetify.warning(request,"Sorry! Requested number of seats is not available")
            return redirect("flights")
        booking_obj=Booking.objects.create(flight=flight_obj,customer=request.user,status=Booking.INITIATED)
        for i in range(1,int(seats)+1):
            first_name=request.POST[f"first_name_{ i }"]
            last_name=request.POST[f"last_name_{i}"]
            gender=request.POST[f"gender_{i}"]
            age=request.POST[f"age_{i}"]
            seat_objs=Seat.objects.filter(flight=flight_obj,status=Seat.AVAILABLE)
            seat_obj=seat_objs[0]
            Passenger.objects.create(first_name=first_name,last_name=last_name,gender=int(gender),seat_id=seat_obj,booking=booking_obj)
            seat_obj.status=Seat.BOOKED
            seat_obj.save()
        
        
        return render(request,"flights/pay.html",{"key":conf_settings.STRIPE_PUBLISHABLE_KEY,"booking_id":booking_obj.id})

def pay(request):
    if request.method=="POST":
        print(request.POST)
        print("yesssssssssss")
        booking_id=request.POST["booking_id"]
        booking_obj=Booking.objects.get(id=booking_id)
        booking_obj.save()
        # charge=stripe.PaymentIntent.create(amount=500,currency="gbp")
        return render(request,"flights/success.html")


    print(conf_settings.STRIPE_PUBLISHABLE_KEY)
    return render(request,"flights/test.html",{"key":conf_settings.STRIPE_PUBLISHABLE_KEY}) 
