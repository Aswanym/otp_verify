from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import phoneModel
import base64
from .serializers import *
from rest_framework import status
from twilio.rest import Client
from private import ACCOUNT_SID,AUTH_TOKEN,TWILIO_PHONENUMBER
# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

class UserLoginAV(APIView):
     def post(self, request):

        phonenumber = request.data['phone']
        phone = phonenumber[3:]
        print(phonenumber)
        print("phone",phone)
        try:
            Mobile = phoneModel.objects.get(Mobile=phonenumber)
        except ObjectDoesNotExist:
            serializer = UserSerializer(data={"Mobile":phonenumber})
            if serializer.is_valid():
                serializer.save()
                Mobile = phoneModel.objects.get(Mobile=phonenumber)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        Mobile.counter += 1  # Update Counter At every Call
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(Mobile.counter))
        otps =  OTP.at(Mobile.counter)

        try:
            account_sid = ACCOUNT_SID
            auth_token = AUTH_TOKEN
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                                        body= "Your Whitelabel verification code is: "+otps,
                                        from_=TWILIO_PHONENUMBER,
                                        to=phonenumber
                                    )
            return Response({"message":"success","twilio status":message.status}, status=200)  # Just for demonstration
        except:
            return Response({"message":"error","twilio status":message.status}, status=400)
        
class CheckOtpAV(APIView):
    def post(self, request):

        phonenumber = request.data['phone']
        otp = request.data['otp']
        phone = phonenumber[3:]
        try:
            Mobile = phoneModel.objects.get(Mobile=phonenumber)
        except ObjectDoesNotExist:
            return Response({"message":"error"}, status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(otp, Mobile.counter):  # Verifying the OTP
            if Mobile.isVerified == False:
                Mobile.isVerified = True
                Mobile.save()
                return Response({"message":"welcome"}, status=200)
            return Response({"message":"welcome back","userid":Mobile.id}, status=200)
        return Response({"message":"invalid"}, status=400)

