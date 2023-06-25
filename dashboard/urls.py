from django.urls import path
from . import views

urlpatterns=[
    # path("",views.dashboard,name="dashboard"),
    path("airlines/",views.airlines,name="airlines"),
    path("airports/",views.airports,name="airports"),
    path("flights/",views.dashboard_flights,name="dashboard_flights")
]