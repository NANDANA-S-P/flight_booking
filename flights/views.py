from django.shortcuts import render,redirect
from users.models import Profile
# Create your views here.

def flights(request):
    if request.user.is_authenticated:
        profile_obj=Profile.objects.filter(user=request.user)
        if profile_obj:
            return render(request,"flights/flights.html")
        else:
            return redirect("details")
    else:
        return redirect("login")
    
