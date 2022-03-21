from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

# this model Stores the data of the Phones Verified
class phoneModel(models.Model):
    Mobile = PhoneNumberField()
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)   # For HOTP Verification

    def __str__(self):
        return str(self.Mobile)