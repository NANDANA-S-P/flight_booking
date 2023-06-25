from django.shortcuts import render,redirect
from users.models import Profile
from flights.models import Flight, Airport,Seat, Booking,Passenger
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
import sweetify
from django.conf import settings as conf_settings
import stripe
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


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
            return render(request,"flights/flights.html",{"airports":airports,"flights":flight_details})
        
        else:
            return redirect("details")
    else:
        return redirect("login")
    

@login_required()
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
    return redirect("flights")

@login_required()
def confirm_booking(request):
    if request.method=="POST":
        seats=request.POST["seats"]
        flight_id=request.POST["flight_id"]
        flight_obj=Flight.objects.get(id=flight_id)
        available_seats=Seat.objects.filter(status=0,flight=flight_obj).count()
        if(int(seats)>available_seats):
            sweetify.warning(request,"Sorry! Requested number of seats is not available")
            return redirect("flights")
        booking_obj=Booking.objects.create(flight=flight_obj,customer=request.user,status=Booking.INITIATED,date_time=datetime.now())
        for i in range(1,int(seats)+1):
            first_name=request.POST[f"first_name_{ i }"]
            last_name=request.POST[f"last_name_{i}"]
            try:
                gender=request.POST[f"gender_{i}"]
            except:
                gender=3
            age=request.POST[f"age_{i}"]
            seat_objs=Seat.objects.filter(flight=flight_obj,status=Seat.AVAILABLE)
            seat_obj=seat_objs[0]
            Passenger.objects.create(first_name=first_name,last_name=last_name,gender=int(gender),seat_id=seat_obj,booking=booking_obj,age=int(age))
            seat_obj.status=Seat.BOOKED
            seat_obj.save()
        
        print("fare is",booking_obj.flight.fare*int(seats))
        return render(request,"flights/pay.html",{"key":conf_settings.STRIPE_PUBLISHABLE_KEY,"booking_id":booking_obj.id,"fare":booking_obj.flight.fare*int(seats)*100})

@login_required()
def pay(request):
    if request.method=="POST":
        print(request.POST)
        booking_id=request.POST["booking_id"]
        booking_obj=Booking.objects.get(id=booking_id)
        booking_obj.status=Booking.PAID
        booking_obj.date_time=datetime.now()
        booking_obj.save()
        # charge=stripe.PaymentIntent.create(amount=500,currency="gbp")
        return render(request,"flights/success.html")


    print(conf_settings.STRIPE_PUBLISHABLE_KEY)
    return render(request,"flights/test.html",{"key":conf_settings.STRIPE_PUBLISHABLE_KEY}) 


@login_required()
def my_bookings(request):
    bookings=Booking.objects.filter(customer=request.user).exclude(status=Booking.INITIATED)
    print(bookings)
    return render(request,"flights/my_bookings.html",{"bookings":bookings})

@login_required()
def my_booking_detail(request,booking_id):
    booking_obj=Booking.objects.get(id=booking_id)
    seats=booking_obj.associated_passengers.all().count()
    if(booking_obj.customer!=request.user) or booking_obj.status==Booking.INITIATED:
        sweetify.warning(request,"Invalid access",button="OK")
        return redirect("my_bookings")
    is_cancellation_available=False
    if booking_obj.status==Booking.PAID and timezone.now() < booking_obj.flight.departure:
        is_cancellation_available=True
    if request.method=="POST":
        booking_obj.status=Booking.CANCELLED
        booking_obj.save()
        print("haaaaaaan")
    return render(request,"flights/my_booking_detail.html",{"booking_obj":booking_obj,"fare":(booking_obj.flight.fare)*int(seats),"passengers":booking_obj.associated_passengers.all(),"is_cancellation_available":is_cancellation_available})

@login_required()
def download_booking(request,booking_id):
    booking_obj=Booking.objects.get(id=booking_id)
    if(booking_obj.customer!=request.user) or booking_obj.status==Booking.INITIATED:
        sweetify.warning(request,"Invalid access",button="OK")
        return redirect("my_bookings")
    
    template_path = 'flights/download_booking.html'
    response = HttpResponse(content_type='application/pdf')
    file_name = "Skygrab_booking.pdf"
    response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
    template = get_template(template_path)
    all_passengers=[]
    for p in booking_obj.associated_passengers.all():
        all_passengers.append(p)
    context = {
       
        "booking":booking_obj,
        "passenger":all_passengers

    }
    print(all_passengers)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
