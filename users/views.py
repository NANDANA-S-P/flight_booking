from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.\
import sweetify
import math,random

def login(request):
    if request.method=="POST":
        if 'login_button' in request.POST:
            username=request.POST['email']
            password=request.POST['password']
            # print(email,password,"logininn")
            user = authenticate(username = username, password = password)
            if user is not None:
                auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
                return redirect("flights")
            else:
                sweetify.warning(request,"<p style='font-size:20px'>Invalid credentials</p>",button="OK")
                return redirect("login")
        if 'otp_button' in request.POST:
            email=request.POST['email']
            print(email,"otppppp")
            user_obj=User.objects.filter(email=email)
            if user_obj:
                profile_obj=Profile.objects.filter(user=user_obj[0])
                if profile_obj:
                    sweetify.info(request,"Account already exists with this email!")
                    return redirect("login")
            
            digits = "0123456789"
            otp_number = ""
            for i in range(6) :
                otp_number += digits[math.floor(random.random() * 10)]
            OTP.objects.create(email=email,otp_number=otp_number)
            #send mail here
            print(otp_number)
            return redirect("details")





    return render(request,"users/new_login.html")


@csrf_exempt
def send_otp(request):

    print("yeah reached dude")
    email=request.GET['email']
    print(email,"otppppp")
    user_obj=User.objects.filter(email=email)
    if user_obj:
        profile_obj=Profile.objects.filter(user=user_obj[0])
        if profile_obj:
            sweetify.info(request,"Account already exists with this email!")
            return redirect("login")
    
    digits = "0123456789"
    otp_number = ""
    for i in range(6) :
        otp_number += digits[math.floor(random.random() * 10)]
    existing_otps=OTP.objects.filter(email=email)
    if existing_otps:
        existing_otps.delete()
    OTP.objects.create(email=email,otp_number=otp_number)
    #send mail here
    print(otp_number)
    return JsonResponse({"status":200})
    
        
        # return 1

def verify_account(request,email):
    return render(request,"users/otp.html")


def logout_user(request):
    logout(request)
    return redirect('login')

def details(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method=="POST":
        user=request.user
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        phone_number=request.POST["phone_number"]
        Profile.objects.create(first_name=first_name,last_name=last_name,phone_number=phone_number,user=request.user,age=0)
        sweetify.success(request,"Profile created successfully!",button="OK")
        return redirect("flights")
    return render(request,"users/details.html")