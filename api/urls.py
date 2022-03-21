from django.urls import path, include
from .views import *

urlpatterns = [

    path("userlogin/", UserLoginAV.as_view(), name="userlogin"),
    path("otpcheck/", CheckOtpAV.as_view(), name="otpcheck"),
]