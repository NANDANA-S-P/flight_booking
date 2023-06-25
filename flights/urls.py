from django.urls import path,include
from . import views

urlpatterns=[
    path("",views.flights,name="flights"),
    path("book/",views.book,name="book"),
    path("confirm_booking/",views.confirm_booking,name="confirm_booking"),
    path("pay/",views.pay,name="pay_test"),
    path("my_bookings/",views.my_bookings,name="my_bookings"),
    path("my_booking_detail/<str:booking_id>/",views.my_booking_detail,name="my_booking_detail"),
    path("download_booking/<str:booking_id>/",views.download_booking,name="download_booking")
]