from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(All_Images)
admin.site.register(UserProfile)
admin.site.register(Account_Otp)
admin.site.register(Lgin_otp)
admin.site.register(UserHistory)