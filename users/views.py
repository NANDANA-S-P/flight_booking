from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .models import *
from django.views.decorators.csrf import csrf_exempt
from social_django.models import UserSocialAuth


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

        if "register_button" in request.POST:
            email=request.POST["email"]
            password1=request.POST["password1"]
            password2=request.POST["password2"]
            user_obj=User.objects.filter(email=email)
            if user_obj:
                sweetify.warning(request,"Account already exists!",button="OK")
                return redirect("login")                    
            user_obj=User.objects.create(email=email,username=email)
            user_obj.set_password(password1)
            user_obj.save()
            user = authenticate(username = email, password = password1)
            auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')




            
            
            
           
            #send mail here
            




    return render(request,"users/new_login.html")


# @csrf_exempt
# def send_otp(request,email):

#     print("yeah reached dude")
#     # email=request.GET['email']
#     print(email,"otppppp")
#     user_obj=User.objects.filter(email=email)
#     if user_obj:
#         profile_obj=Profile.objects.filter(user=user_obj[0])
#         if profile_obj:
#             sweetify.info(request,"Account already exists with this email!")
#             return redirect("login")
    
    
    
        
        # return 1

def verify(request):
    profile_obj=Profile.objects.filter(user=request.user)
    if profile_obj:
        sweetify.info(request,"Account already exists!")
        return redirect("login")
    if request.method=="GET":
        digits = "0123456789"
        otp_number = ""
        for i in range(6) :
            otp_number += digits[math.floor(random.random() * 10)]
        existing_otps=OTP.objects.filter(email=request.user.email)
        if existing_otps:
            existing_otps.delete()
        OTP.objects.create(email=request.user.email,otp_number=otp_number)
        #send mail here
        print(otp_number)
    

    return render(request,"users/otp.html")


def logout_user(request):
    logout(request)
    return redirect('login')

def details(request):
    print("yea[]")
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method=="POST":
        if "verify_btn" in request.POST:       
            otp_obj=OTP.objects.get(email=request.user.email)
            otp_value=request.POST["otp"]
            if(otp_value==str(otp_obj.otp_number)):
                sweetify.success(request,"Account verified!")
                return redirect("details")
            else:
                sweetify.warning(request,"Invalid OTP")
                return redirect("verify")
        if "reg_btn" in request.POST:
            print("ohhh")
            user=request.user
            first_name=request.POST["first_name"]
            last_name=request.POST["last_name"]
            phone_number=request.POST["phone_number"]
            Profile.objects.create(first_name=first_name,last_name=last_name,phone_number=phone_number,user=request.user)
            sweetify.success(request,"Profile created successfully!",button="OK")
            return redirect("flights") 
    return render(request,"users/details.html")
   