from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib.auth import logout
# Create your views here.\
import sweetify

def login(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        password=request.POST["password"]
        confirm_password=request.POST["confirm_password"]
        user_obj=CustomUser.objects.filter(email=email)
        if user_obj:
            if user_obj.is_verified==False:
                return redirect()
        #validations
        CustomUser.objects.create(username=email,first_name=name,email=email,password=password)
        sweetify.success(request,"Check your email for account verification!",button="OK")
        print(name,email,password,confirm_password)


    return render(request,"users/login.html")

def verify_account(request,email):
    return render(request,"users/otp.html")


def logout_user(request):
    logout(request)
    return redirect('landing_page')