from django.urls import path
from . import views

urlpatterns=[
    # path("",views.dashboard,name="dashboard"),
    path("airlines/",views.airlines,name="airlines"),
    path("airports/",views.airports,name="airports"),
    path("flights/",views.dashboard_flights,name="dashboard_flights"),
    path("bookings/",views.bookings,name="bookings"),
    path("booking_detail/<str:flight_id>/",views.booking_detail,name="booking_detail"),
    path("passenger_details/<str:booking_id>/",views.passenger_details,name="passenger_details")
]