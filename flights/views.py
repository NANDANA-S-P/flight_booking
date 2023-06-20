from django.shortcuts import render

# Create your views here.
def flights(request):
    if request.user.is_authenticated:
        if request.user.is_verified:
            return render(request,"flights/flights.html")
        else:
            #get details
            pass
    return render(request,"flights/flights.html")