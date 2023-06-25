from django.urls import path,include
from . import views

urlpatterns=[
    path("",views.flights,name="flights"),
    path("book/",views.book,name="book"),
    path("confirm_booking/",views.confirm_booking,name="confirm_booking"),
    path("pay/",views.pay,name="pay_test")
]