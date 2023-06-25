from django.urls import path
from users import views

urlpatterns=[
    path("login/",views.login,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path("details/",views.details,name="details"),

]